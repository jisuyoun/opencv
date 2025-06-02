// CSRF 토큰을 쿠키에서 읽어옴
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var defects = []; // 조회된 불량 정보
var nowIndex = 0; // 현재 보여지고 있는 인덱스

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
    

    //var nowDefects = [];

    const defectsDataElement = document.getElementById('defects-data');
    if (defectsDataElement) {
        try {
            defects = JSON.parse(defectsDataElement.textContent);
            //nowDefects = defects[0];
        } catch (error) {
            console.error("불량 기록 데이터 파싱 중 오류 발생:", error);
        }
    } else {
        console.warn("defects-data 스크립트 태그를 찾을 수 없습니다.");
    }

    displayDefects(0);

});


function displayDefects(index) {
    if (index < 0 || index >= defects.length) {
        console.log("유효하지 않은 인덱스 발생: " + index)
        return;
    }

    const currentDefect = defects[index];
    
    // 이미지 변경
    const defectImageElement = document.getElementById("product-image");
    if (defectImageElement) {
        if (currentDefect.web_image_url) {
            defectImageElement.src = currentDefect.web_image_url;
            defectImageElement.alt = currentDefect.defect_type || '불량 이미지';
        } else {
            defectImageElement.src = '';
            defectImageElement.alt = '이미지 없음';
        }
    }

    $("#fileInfo").text(currentDefect.web_image_url);
    $("#dateInfo").text(currentDefect.timestamp);
    $("#typeInfo").text(currentDefect.defect_type);
    $("#messageInfo").text(currentDefect.message);
    $("#topDate").text(currentDefect.timestamp);

    const backButton = document.querySelector("#back-btn");
    const nextButton = document.querySelector("#next-btn");
  
    nowIndex = index;

    if (nowIndex === 0) {
        backButton.disabled = true;
    } else {
        backButton.disabled = false;
    }

    if (nowIndex === (defects.length - 1)) {
        nextButton.disabled = true;
    } else {
        nextButton.disabled = false;
    }
}

// 이전 정보
function moveBack() {
    let backIndex = nowIndex - 1;
    displayDefects(backIndex);
}

// 다음 정보
function moveNext() {
    let nextIndex = nowIndex + 1;
    displayDefects(nextIndex);
}

// 새로고침
function reload() {
    window.location.reload();
}

// 불량 확정
function confirmDefect() {
    const currentId = defects[nowIndex].id;

    if (!currentId) {
        alert("불량 확정을 할 아이디가 조회되지 않습니다.")
        return;
    }

    const dataToConfirm = {
        confirm_id: currentId
    }

    fetch("/api/confirm_defect/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(dataToConfirm)
    }).then(responseData => {
        alert("불량 확정이 완료되었습니다.")
        defects.splice(nowIndex, 1);

        if (nowIndex >= defects.length && defects.length > 0) {
            nowIndex = defects.length - 1;
        } else if (defects.length == 0) {
            nowIndex = 0;
        }

        displayDefects(nowIndex)

    }).then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                console.error("불량 확정 API 오류:", errorData);
                throw new Error(`HTTP 오류: ${response.status}, 상세: ${JSON.stringify(errorData)}`);
            });
        }
        return response.json();
    }).catch(error => {
        console.error("불량 확정 요청 중 오류 발생: ", error);
        alert("불량 확정 실패: " + error.message)
    });
}