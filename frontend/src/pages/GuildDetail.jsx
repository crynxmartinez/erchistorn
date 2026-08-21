import { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

export default function GuildDetail() {
    const navigate = useNavigate();
    const { guildId } = useParams();

    useEffect(() => {
        navigate("/guild-house", { replace: true });
    }, [navigate, guildId]);

    return null;
}
