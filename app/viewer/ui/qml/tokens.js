.pragma library

function phaseColor(phaseRaw, colors) {
    var p = (phaseRaw || "").toLowerCase();
    if (p.indexOf("move") >= 0 || p.indexOf("движ") >= 0)
        return colors.movement || "#2f6ed8";
    if (p.indexOf("shoot") >= 0 || p.indexOf("стрел") >= 0)
        return colors.shooting || "#b88a26";
    if (p.indexOf("charge") >= 0 || p.indexOf("заряд") >= 0)
        return colors.charge || "#d97706";
    if (p.indexOf("fight") >= 0 || p.indexOf("бой") >= 0)
        return colors.fight || "#cf3f3f";
    if (p.indexOf("command") >= 0)
        return colors.command || "#6f7d92";
    return colors.defaultPhase || "#98a4b8";
}

function phaseIcon(phaseRaw) {
    var p = (phaseRaw || "").toLowerCase();
    if (p.indexOf("move") >= 0 || p.indexOf("движ") >= 0) return "👣";
    if (p.indexOf("shoot") >= 0 || p.indexOf("стрел") >= 0) return "🎯";
    if (p.indexOf("charge") >= 0 || p.indexOf("заряд") >= 0) return "⚡";
    if (p.indexOf("fight") >= 0 || p.indexOf("бой") >= 0) return "⚔️";
    return "▶";
}

function sideColor(sideRaw, playerColor, modelColor) {
    var s = (sideRaw || "").toLowerCase();
    if (s === "player" || s === "enemy") return playerColor;
    if (s === "model") return modelColor;
    return "#98a4b8";
}
