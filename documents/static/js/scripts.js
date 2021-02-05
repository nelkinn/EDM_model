/*function showDisplay()
        { document.getElementById("doc_display").style.display ="block";}*/

function showFrame() {
    if($(".frameOn").is(":focus"))
    {
        $( ".test" ).show();
        }
}


$(document).ready(function () {
   var url=document.location.href;
   console.log(url);
          $.each($(".menu a"),function(){
    if(this.href==url){$(this).parent().addClass('active');};
   });
});



/*$(function(){
    $(".doc_block").click(function() {
        $( ".doc_display" ).visible();
    })
}*/

/*function showDisplay() {
    if($(".doc_block").is(":focus"))
    {
        $('.Класс_фрейма').attr('src', 'Нужная ссылка');
        }*/
