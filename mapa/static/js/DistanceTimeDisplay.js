document.addEventListener("DOMContentLoaded", function () {
    const e = React.createElement;

    function DistanceTimeDisplay() {
        const [distance, setDistance] = React.useState("0 km");
        const [duration, setDuration] = React.useState("0 min");

        window.updateDistanceTime = (newDistance, newDuration) => {
            setDistance(newDistance);
            setDuration(newDuration);
        };

        return e("div", { style: { padding: "10px", background: "white", borderRadius: "8px", width: "300px", position: "absolute", top: "180px", left: "20px", zIndex: "10" } }, [
            e("p", { key: "dist", style: { fontWeight: "bold" } }, `📍 Distância: ${distance}`),
            e("p", { key: "time", style: { fontWeight: "bold" } }, `⏳ Tempo Estimado: ${duration}`)
        ]);
    }

    const root = ReactDOM.createRoot(document.getElementById("react-distance-time"));
    root.render(e(DistanceTimeDisplay));
});
