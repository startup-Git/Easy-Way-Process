/*****************
navbar fixed
*******************/
window.addEventListener('scroll', function() {
  const header = document.getElementById('navbar');
  const sticky = header.offsetTop;

  if (window.pageYOffset > sticky) {
      header.classList.add('sticky');
  } else {
      header.classList.remove('sticky');
  }
});
/*****************
navbar fixed
*******************/
// Testimonial Slider
let testimonialIndex = 1
ShowTestimonial(testimonialIndex)

function plusTestimonial(n) {
  ShowTestimonial(testimonialIndex += n)
}
function currentTestimonial(n){
  ShowTestimonial(testimonialIndex = n)
}

function ShowTestimonial(n){
  let i
  let slider = document.getElementsByClassName('slider')
  let dots = document.getElementsByClassName('dot')

  if(n > slider.length){
    testimonialIndex = 1
  }
  if(n < 1){
    testimonialIndex = slider.length
  }

  for( i = 0; i < slider.length; i++){
    slider[i].style.display = 'none'
  }
  for( i = 0; i < dots.length; i++){
    dots[i].className = dots[i].className.replace(" dot_active", "")
  }
  slider[testimonialIndex-1].style.display = "block"
  slider[testimonialIndex-1].className += " show"
  dots[testimonialIndex-1].className += " dot_active"

}