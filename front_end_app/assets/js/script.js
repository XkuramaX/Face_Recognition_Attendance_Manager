$('#mega-dropdown-btn1,#mega-dropdown-btn2').click(()=>{
    $('.mega-dropdown').toggle();
})
$('.search-top').find('.close').click(()=>{
    $('.mega-dropdown').hide();
})
$('.mega-dropdown li').click((event)=>{
    Console.log($(event.target)[0].innerHTML);
    $('.mega-dropdown').hide();
})