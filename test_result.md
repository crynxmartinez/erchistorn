#====================================================================================================
# START - Testing Protocol - DO NOT EDIT OR REMOVE THIS SECTION
#====================================================================================================

# THIS SECTION CONTAINS CRITICAL TESTING INSTRUCTIONS FOR BOTH AGENTS
# BOTH MAIN_AGENT AND TESTING_AGENT MUST PRESERVE THIS ENTIRE BLOCK

# Communication Protocol:
# If the `testing_agent` is available, main agent should delegate all testing tasks to it.
#
# You have access to a file called `test_result.md`. This file contains the complete testing state
# and history, and is the primary means of communication between main and the testing agent.
#
# Main and testing agents must follow this exact format to maintain testing data. 
# The testing data must be entered in yaml format Below is the data structure:
# 
## user_problem_statement: {problem_statement}
## backend:
##   - task: "Task name"
##     implemented: true
##     working: true  # or false or "NA"
##     file: "file_path.py"
##     stuck_count: 0
##     priority: "high"  # or "medium" or "low"
##     needs_retesting: false
##     status_history:
##         -working: true  # or false or "NA"
##         -agent: "main"  # or "testing" or "user"
##         -comment: "Detailed comment about status"
##
## frontend:
##   - task: "Task name"
##     implemented: true
##     working: true  # or false or "NA"
##     file: "file_path.js"
##     stuck_count: 0
##     priority: "high"  # or "medium" or "low"
##     needs_retesting: false
##     status_history:
##         -working: true  # or false or "NA"
##         -agent: "main"  # or "testing" or "user"
##         -comment: "Detailed comment about status"
##
## metadata:
##   created_by: "main_agent"
##   version: "1.0"
##   test_sequence: 0
##   run_ui: false
##
## test_plan:
##   current_focus:
##     - "Task name 1"
##     - "Task name 2"
##   stuck_tasks:
##     - "Task name with persistent issues"
##   test_all: false
##   test_priority: "high_first"  # or "sequential" or "stuck_first"
##
## agent_communication:
##     -agent: "main"  # or "testing" or "user"
##     -message: "Communication message between agents"

# Protocol Guidelines for Main agent
#
# 1. Update Test Result File Before Testing:
#    - Main agent must always update the `test_result.md` file before calling the testing agent
#    - Add implementation details to the status_history
#    - Set `needs_retesting` to true for tasks that need testing
#    - Update the `test_plan` section to guide testing priorities
#    - Add a message to `agent_communication` explaining what you've done
#
# 2. Incorporate User Feedback:
#    - When a user provides feedback that something is or isn't working, add this information to the relevant task's status_history
#    - Update the working status based on user feedback
#    - If a user reports an issue with a task that was marked as working, increment the stuck_count
#    - Whenever user reports issue in the app, if we have testing agent and task_result.md file so find the appropriate task for that and append in status_history of that task to contain the user concern and problem as well 
#
# 3. Track Stuck Tasks:
#    - Monitor which tasks have high stuck_count values or where you are fixing same issue again and again, analyze that when you read task_result.md
#    - For persistent issues, use websearch tool to find solutions
#    - Pay special attention to tasks in the stuck_tasks list
#    - When you fix an issue with a stuck task, don't reset the stuck_count until the testing agent confirms it's working
#
# 4. Provide Context to Testing Agent:
#    - When calling the testing agent, provide clear instructions about:
#      - Which tasks need testing (reference the test_plan)
#      - Any authentication details or configuration needed
#      - Specific test scenarios to focus on
#      - Any known issues or edge cases to verify
#
# 5. Call the testing agent with specific instructions referring to test_result.md
#
# IMPORTANT: Main agent must ALWAYS update test_result.md BEFORE calling the testing agent, as it relies on this file to understand what to test next.

#====================================================================================================
# END - Testing Protocol - DO NOT EDIT OR REMOVE THIS SECTION
#====================================================================================================



#====================================================================================================
# Testing Data - Main Agent and testing sub agent both should log testing data below this section
#====================================================================================================

user_problem_statement: |
  User pulled an existing "Erchis — Fantasy Dice RPG" game from their GitHub (originally built for
  Vercel deployment with MongoDB Atlas) and wants to launch it on the Emergent environment using
  Emergent resources — specifically the local Emergent MongoDB. Goal: adapt the DB connection and
  get the full-stack game running on the Emergent preview.

backend:
  - task: "MongoDB connection adapted for Emergent local DB (conditional TLS)"
    implemented: true
    working: true
    file: "backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
        - working: true
          agent: "main"
          comment: "Original code forced tls=True, tlsAllowInvalidCertificates=True (for Atlas). Local Emergent Mongo (mongodb://localhost:27017) does not speak TLS and failed the SSL handshake. Made TLS conditional: skip TLS for localhost/127.0.0.1, keep it for remote/Atlas. Verified via curl: /api/health healthy, /api/auth/register wrote a user (200), /api/auth/me read it back via cookie (200), mongosh confirmed the doc in test_database.users. Test user cleaned up afterwards."
        - working: true
          agent: "testing"
          comment: "Comprehensive smoke test completed successfully. Tested: (1) Auth flow - register (200), GET /api/auth/me (200), logout (200), login (200) all working with cookie-based JWT. (2) Character creation - fetched all game data endpoints (races, roles, masteries, origins), created human knight character 'Theron Stormbreaker' (200), verified persistence in MongoDB. (3) Game action - performed explore action in golden_plains biome (200), verified state change (inventory increased from 8 to 10 items, gold changed to 87), confirmed persistence in MongoDB. All endpoints returning correct HTTP codes, data persisting correctly in Emergent local MongoDB. Verified in mongosh: user document exists in test_database.users, character document exists in test_database.characters with correct state."

metadata:
  created_by: "main_agent"
  version: "1.0"
  test_sequence: 1
  run_ui: false

test_plan:
  current_focus:
    - "MongoDB connection adapted for Emergent local DB (conditional TLS)"
  stuck_tasks: []
  test_all: false
  test_priority: "high_first"

agent_communication:
    - agent: "main"
      message: "Launched the pre-built Erchis RPG on Emergent. Only change made was the MongoDB connection (conditional TLS so it works with the local Emergent Mongo instead of Atlas). Please run a FOCUSED SMOKE TEST to confirm the game works end-to-end against the Emergent database: (1) auth flow — register a new user, login, GET /api/auth/me, logout; (2) character creation flow — fetch character-creation data endpoints and create a character; (3) one game action (e.g. an action/hunt/gather or whatever the core play loop endpoint is) and confirm state persists (re-fetch character shows the change). Do NOT attempt an exhaustive test of every one of the dozens of endpoints — the game logic was already tested previously; we only need to confirm persistence works against the Emergent Mongo after the connection change. Report any endpoint returning 500/DB errors."
    - agent: "testing"
      message: "✅ SMOKE TEST COMPLETE - All tests passed! MongoDB persistence working correctly on Emergent environment. Auth flow (register/login/logout/me), character creation (with all game data endpoints), and game actions (explore) all functioning properly. Data verified in MongoDB: users and characters collections contain correct documents with proper state persistence. No 500 errors or DB connection issues encountered. The conditional TLS fix is working as expected."