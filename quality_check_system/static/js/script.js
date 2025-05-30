// 페이지 로드 시 현재 시간 표시
document.addEventListener('DOMContentLoaded', function() {
    const currentTimeSpan = document.getElementById('currentTime');
    if (currentTimeSpan) {
        function updateTime() {
            const now = new Date();
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            const seconds = String(now.getSeconds()).padStart(2, '0');
            currentTimeSpan.textContent = `${hours}:${minutes}:${seconds}`;
        }
        updateTime();
        setInterval(updateTime, 1000);
    }
    console.log("--------------")
    const defectsDataElement = document.getElementById('defects_data');
    //const defectsJsonString = defectsDataElement.textContent;
    //const defects = JSON.parse(defectsJsonString);
    console.log(defectsDataElement); 
});
