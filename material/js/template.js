// input 點擊出現齒輪聲音
function playPause() {
    var music = document.getElementById('music2');
    if (music.paused) {
        music.play();
    }
}
// 進入網頁後撥放音樂
$(function() {
    var myAuto = document.getElementById('myaudio');
    myAuto.play();
})