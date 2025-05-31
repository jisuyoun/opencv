var nowId = "";

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
        const defectsDataElement = document.getElementById('defects-data');
    let defects = []; // 기본값: 빈 배열
    if (defectsDataElement) {
        try {
            defects = JSON.parse(defectsDataElement.textContent);
            defects.forEach (function(item) {
                console.log("불량 기록 데이터:", item); 
            })
        } catch (error) {
            console.error("불량 기록 데이터 파싱 중 오류 발생:", error);
        }
    } else {
        console.warn("defects-data 스크립트 태그를 찾을 수 없습니다.");
    }
});
