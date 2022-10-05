$(document).ready(function () {
  var trigger = $('.hamburger'),
      overlay = $('.overlay'),
     isClosed = false;

    trigger.click(function () {
      hamburger_cross();
    });

    function hamburger_cross() {

      if (isClosed == true) {
        overlay.hide();
        trigger.removeClass('is-open');
        trigger.addClass('is-closed');
        isClosed = false;
      } else {
        overlay.show();
        trigger.removeClass('is-closed');
        trigger.addClass('is-open');
        isClosed = true;
      }
  }

  $('[data-toggle="offcanvas"]').click(function () {
        $('#wrapper').toggleClass('toggled');
  });
});



function AllProduct(category_id){
  console.log(category_id)
  $.get('/home/category/' , {category_id}).then(response => {
    if (response.status === 'unsuccessful'){
        console.log("NO")
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'No product found!',
        })
    }else{
      $(".select-category").html(response.product_html)
      $(".cd-dropdown-trigger").removeClass('dropdown-is-active')
      $(".cd-dropdown").removeClass('dropdown-is-active')
      $(".more").css('display', 'inline')
      $("#tag-cat").html(response.category)
      $("#tag-cat").css('display', 'inline')

    }


  })
}


function ChangeImage(image_id) {

  let image_url = document.getElementById(image_id).value
  $(".img-dt").attr('src' , image_url)
}


function Decrease() {
  var quantity = parseInt($("#inpt").val())
  if (isNaN(quantity)){
    $("#inpt").val(1)
  }else{
    if (quantity > 0){
      $("#inpt").val(quantity-1)
    }
  }

}

function Increase() {
  var quantity = parseInt($("#inpt").val())
  if (isNaN(quantity)){
    $("#inpt").val(1)
  }else{
    $("#inpt").val(quantity+1)
    $("#plus").css('border' , 'none')
  }

}















(function ($) {
    "use strict";


    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input100');

    $('.validate-form').on('submit',function(){
        var check = true;

        for(var i=0; i<input.length; i++) {
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
            }
        }

        return check;
    });


    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function validate (input) {
        if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else {
            if($(input).val().trim() == ''){
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }



})(jQuery);


function AddtoCart(data) {
    var csrftoken = $('input[name=csrfmiddlewaretoken]').val()
    let quantity = $("#inpt").val()
    let product_id=data.product_id
    let check = isNaN(quantity)
    if (check === true){
        return
    }else{
        if (quantity <=0){
            quantity=1
        }
    }

    $.ajax({
        method: 'POST',
        url : '/addtocart/',
        data : {
            'quantity':quantity ,
            'product_id' : product_id ,
            csrfmiddlewaretoken:csrftoken
        },
        success:function (response) {
            if (response.status === 'successful'){
                const Toast = Swal.mixin({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 1700,
                timerProgressBar: true,
                didOpen: (toast) => {
                    toast.addEventListener('mouseenter', Swal.stopTimer)
                    toast.addEventListener('mouseleave', Swal.resumeTimer)
                  }
                })

                Toast.fire({
                  icon: 'success',
                  title: 'Product Added To Cart'
                })
                $("#count-p").html(response.count_p)
            }else if (response.status === 'There is not enough stock'){
                Swal.fire({
                  position: 'top-end',
                  icon: 'error',
                  title: 'There is not enough stock!',
                  timer: 1700
                })
            }else if (response.status === 'product not found') {
                Swal.fire({
                  position: 'top-end',
                  icon: 'error',
                  title: 'Product not found',
                  timer: 1400
                })
            }else if (response.status === 'userid not found'){
                Swal.fire({
                  position: 'top-end',
                  icon: 'error',
                  title: 'You are not logged in',
                  timer: 1450
                })
            }
        }


    })

}



// fetch('/addtocart/', {
//         'method':'POST',
//         'headers':{
//             'Content-Type': 'application/json',
//             'X-CSRFToken':csrftoken
//         },
//         body:JSON.stringify({'quantity':quantity , 'product_id' : product_id})
//     }).then(response => {
//         return response.json()
//     }).then(data => {
//         if (data.status === 'successful'){
//             const Toast = Swal.mixin({
//             toast: true,
//             position: 'top-end',
//             showConfirmButton: false,
//             timer: 1700,
//             timerProgressBar: true,
//             didOpen: (toast) => {
//                 toast.addEventListener('mouseenter', Swal.stopTimer)
//                 toast.addEventListener('mouseleave', Swal.resumeTimer)
//               }
//             })
//
//             Toast.fire({
//               icon: 'success',
//               title: 'Product Added To Cart'
//             })
//             $("#count-p").html(data.count_p)
//         }else {
//             Swal.fire({
//               position: 'top-end',
//               icon: 'error',
//               title: 'Product not found',
//               timer: 1400
//             })
//         }
//     })


function RemoveProduct(id) {
    $.get("/remove-product/" ,  {'item_id':id}).then(response => {
        if (response.status === 'deleted'){
            console.log(response.item_count)
            $(".htm-js").html(response.cart_detail)
            $("#count-p").html(response.item_count)
        }
    })
}

// function CouponApply() {
//
//     var discount_code = $("#discount-code").val()
//     var csrftoken = $('input[name=csrfmiddlewaretoken]').val()
//     fetch('/coupon-apply/', {
//         'method':'POST',
//         'headers':{
//             'Content-Type': 'application/json',
//             'X-CSRFToken':csrftoken
//         },
//         body:JSON.stringify({'discount_code':discount_code})
//     }).then(response => {
//         return response.json()
//     }).then(data => {
//         if (data.status === "valid"){
//
//             $(".promo-code-dis").html("<li class=\"list-group-item d-flex justify-content-between\" style=\"border-radius:0\">\n" +
//                 "              <span>Total (USD)</span>\n" +
//                 "              <strong id=\"total-pr\">$</strong>\n" +
//                 "            </li>\n" +
//                 "            <li class=\"list-group-item d-flex justify-content-between bg-light\" style=\"border-radius:0\">\n" +
//                 "              <div class=\"text-success\">\n" +
//                 "                <h6 class=\"my-0\">Promo code</h6>\n" +
//                 "              </div>\n" +
//                 "              <span class=\"text-danger\" id=\"percent\">-$5</span>\n" +
//                 "            </li>")
//             $("#percent").html(data.persent)
//             $("#final-price").html(data.final_price)
//             $("#total-pr").html(data.total_price)
//             $("#discount-code").val('Discount successfully applied !')
//             $("#discount-code").addClass('disabled')
//             $(".btn-discount").removeClass('btn-discount-failed')
//             $(".btn-discount").addClass('btn-discount-success')
//
//             $(".btn-discount").html('<img src="/static/img/success.png" alt="">')
//             $(".btn-discount").attr('onclick' , '')
//
//
//
//         }else {
//             $("#discount-code").val('The discount code is not valid !')
//             $(".btn-discount").addClass('btn-discount-failed')
//             $(".btn-discount").html('<img src="/static/img/fail.png" alt="">')
//         }
//     })
// }




function CouponApply() {
    var discount_code = $("#discount-code").val()
    var csrftoken = $('input[name=csrfmiddlewaretoken]').val()
    $.ajax({
        method: 'POST',
        url : '/coupon-apply/',
        data : {
            'discount_code':discount_code,
             csrfmiddlewaretoken:csrftoken
        },
        success:function (response) {
            if (response.status === "valid"){

                $(".promo-code-dis").html("<li class=\"list-group-item d-flex justify-content-between\" style=\"border-radius:0\">\n" +
                    "              <span>Total (USD)</span>\n" +
                    "              <strong id=\"total-pr\">$</strong>\n" +
                    "            </li>\n" +
                    "            <li class=\"list-group-item d-flex justify-content-between bg-light\" style=\"border-radius:0\">\n" +
                    "              <div class=\"text-success\">\n" +
                    "                <h6 class=\"my-0\">Promo code</h6>\n" +
                    "              </div>\n" +
                    "              <span class=\"text-danger\" id=\"percent\">-$5</span>\n" +
                    "            </li>")
                $("#percent").html(response.persent)
                $("#final-price").html(response.final_price)
                $("#total-pr").html(response.total_price)
                $("#discount-code").val('Discount successfully applied !')
                $("#discount-code").addClass('disabled')
                $(".btn-discount").removeClass('btn-discount-failed')
                $(".btn-discount").addClass('btn-discount-success')

                $(".btn-discount").html('<img src="/static/img/success.png" alt="">')
                $(".btn-discount").attr('onclick' , '')
                location.reload()


            }else {
                $("#discount-code").val('The discount code is not valid !')
                $(".btn-discount").addClass('btn-discount-failed')
                $(".btn-discount").html('<img src="/static/img/fail.png" alt="">')
            }
        }
    })
}

function ChangeCount(value) {
    console.log(value)
    $.get('/change-count/' , {'status':value.status , 'item_id':value.item_id}).then(response => {
        if (response.status === 'successful'){
            $(".htm-js").html(response.html_code)
        }else {
            Swal.fire({
              position: 'top-end',
              icon: 'error',
              title: 'There is not enough stock!',
              timer: 1700
            })
    }
    })
}

$(".h1-empty").hover(function (){
    $(this).html("< Back To Home")
    $(this).css('padding-left' , '5px')
    $(this).css('width' , '320px')



},function (){
    $(this).css('width' , '400px')
    $(this).html("Your Cart Is Empty !")
    $(this).css('padding-left' , '22px')

})








function ShowPaypal() {
    var firstname = $("#firstname").val()
    var lastname = $("#lastname").val()
    var address = $("#address").val()
    var country = $("#country").val()
    var state = $("#state").val()
    var zip = $("#zip").val()
    var final_price = $("#final-price").val()
    console.log(lastname)
    $("#firstName").removeClass('error-inpt')
    $("#er-firstname").removeClass('error')
    $("#lbl").removeClass('error')
    $("#er-firstname").html('')
    $("#lastname").removeClass('error-inpt')
    $("#er-lastname").removeClass('error')
    $("#er-lastname").html('')
    $("#address").removeClass('error-inpt')
    $("#er-address").removeClass('error')
    $("#er-address").html('')
    $("#country").removeClass('error-inpt')
    $("#er-country").removeClass('error')
    $("#er-country").html('')
    $("#state").removeClass('error-inpt')
    $("#er-state").removeClass('error')
    $("#er-state").html('')
    $("#zip").removeClass('error-inpt')
    $("#er-zip").removeClass('error')
    $("#er-zip").html('')

    if (firstname === '' || firstname === 'undefined'){
        $("#firstName").addClass('error-inpt')
        $("#er-firstname").addClass('error')
        $("#lbl").addClass('error')
        return $("#er-firstname").html('Please complete the field')
    }
    if (lastname === '' || lastname === 'undefined'){
        console.log("LASTNAME")
        $("#lastname").addClass('error-inpt')
        $("#er-lastname").addClass('error')
        $("#lbl").addClass('error')
        return $("#er-lastname").html('Please complete the field')
    }
    if (address === ''){
        $("#address").addClass('error-inpt')
        $("#er-address").addClass('error')
        $("#lbl").addClass('error')
        return $("#er-address").html('Please complete the field')
    }
    if (country === ''){
        $("#country").addClass('error-inpt')
        $("#er-country").addClass('error')
        $("#lbl").addClass('error')
        return $("#er-country").html('Please complete the field')
    }
    if (state === ''){
        $("#state").addClass('error-inpt')
        $("#er-state").addClass('error')
        $("#lbl").addClass('error')
        return $("#er-state").html('Please complete the field')
    }
    if (zip === ''){
        $("#zip").addClass('error-inpt')
        $("#er-zip").addClass('error')
        $("#lbl").addClass('error')
        return $("#er-zip").html('Please complete the field')
    }
    $("#payment-info").removeClass('hidden')
}



function SubmitForm(transaction) {
    if (transaction.status === "COMPLETED"){
        var firstname = $("#firstname").val()
        var lastname = $("#lastname").val()
        var address = $("#address").val()
        var country = $("#country").val()
        var state = $("#state").val()
        var zip = $("#zip").val()
        var transaction_id = transaction.id

        $("#firstname").removeClass('error-inpt')
        $("#er-firstname").removeClass('error')
        $("#lbl").removeClass('error')
        $("#er-firstname").html('')
        $("#lastname").removeClass('error-inpt')
        $("#er-lastname").removeClass('error')
        $("#er-lastname").html('')
        $("#address").removeClass('error-inpt')
        $("#er-address").removeClass('error')
        $("#er-address").html('')
        $("#country").removeClass('error-inpt')
        $("#er-country").removeClass('error')
        $("#er-country").html('')
        $("#state").removeClass('error-inpt')
        $("#er-state").removeClass('error')
        $("#er-state").html('')
        $("#zip").removeClass('error-inpt')
        $("#er-zip").removeClass('error')
        $("#er-zip").html('')

        if (firstname === ''){
            $("#firstname").addClass('error-inpt')
            $("#er-firstname").addClass('error')
            $("#lbl").addClass('error')
            return $("#er-firstname").html('Please complete the field')
        }
        if (lastname === ''){
            $("#lastname").addClass('error-inpt')
            $("#er-lastname").addClass('error')
            $("#lbl").addClass('error')
            return $("#er-lastname").html('Please complete the field')
        }
        if (address === ''){
            $("#address").addClass('error-inpt')
            $("#er-address").addClass('error')
            $("#lbl").addClass('error')
            return $("#er-address").html('Please complete the field')
        }
        if (country === ''){
            $("#country").addClass('error-inpt')
            $("#er-country").addClass('error')
            $("#lbl").addClass('error')
            return $("#er-country").html('Please complete the field')
        }
        if (state === ''){
            $("#state").addClass('error-inpt')
            $("#er-state").addClass('error')
            $("#lbl").addClass('error')
            return $("#er-state").html('Please complete the field')
        }
        if (zip === ''){
            $("#zip").addClass('error-inpt')
            $("#er-zip").addClass('error')
            $("#lbl").addClass('error')
            return $("#er-zip").html('Please complete the field')
        }

        $.get('/check-info/' , {zip , firstname , lastname , address , country , state , total , transaction_id}).then(response => {
            if (response.status === 'successful'){
                Swal.fire({
                  title: 'The order was successfully placed !',
                  icon: 'success',
                  confirmButtonColor: '#3085d6',
                  confirmButtonText: 'OK!'
                })
                setTimeout(()=>{location.href = '/'} , 3000)
            }else {
                Swal.fire({
                  icon: 'error',
                  title: 'Oops...',
                  text: 'Something went wrong!',
                })
            }
        })
    }else {
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'Something went wrong!',
        })
    }



}



// --------------------------------sidebar menu------------------------------------
var btnContainer = document.getElementById("main-div");
console.log(btnContainer)
var btns = btnContainer.getElementsByClassName("bttn");
console.log(btns)

for (var i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("active-side");
    current[0].className = current[0].className.replace(" active-side", "");
    this.className += " active-side";
  });
}

// -------------------------------------sidebar menu--------------------------------------------------------



function Saveinformation() {

        var firstname = $("#firstname").val()
        var lastname = $("#lastname").val()
        var address = $("#address").val()
        var country = $("#country").val()
        var state = $("#state").val()
        var zip = $("#zip").val()

        if (firstname === ''){
            $("#firstname").addClass('error-inpt')
            $("#er-firstname").addClass('error')
            $("#lbl").addClass('error')
            return $("#er-firstname").html('Please complete the field')
        }
        if (lastname === ''){
            $("#lastname").addClass('error-inpt')
            $("#er-lastname").addClass('error')
            $("#lbl").addClass('error')
            return $("#er-lastname").html('Please complete the field')
        }
        if (address === ''){
            $("#address").addClass('error-inpt')
            $("#er-address").addClass('error')
            $("#lbl").addClass('error')
            return $("#er-address").html('Please complete the field')
        }
        if (country === ''){
            $("#country").addClass('error-inpt')
            $("#er-country").addClass('error')
            $("#lbl").addClass('error')
            return $("#er-country").html('Please complete the field')
        }
        if (state === ''){
            $("#state").addClass('error-inpt')
            $("#er-state").addClass('error')
            $("#lbl").addClass('error')
            return $("#er-state").html('Please complete the field')
        }
        if (zip === ''){
            $("#zip").addClass('error-inpt')
            $("#er-zip").addClass('error')
            $("#lbl").addClass('error')
            return $("#er-zip").html('Please complete the field')
        }

        $.get('/profile/edit-info/' , {zip , firstname , lastname , address , country , state}).then(response => {
            if (response.status === 'successful'){
                Swal.fire({
                  title: 'Information Saved Successfully !',
                  icon: 'success',
                  confirmButtonColor: '#3085d6',
                  confirmButtonText: 'OK!'
                })
                $(".contain-info").html(response.html-code)
            }else {
                Swal.fire({
                  icon: 'error',
                  title: 'Oops...',
                  text: 'Something went wrong!',
                })
            }
        })

}

function SaveAvatar() {
    profile_image = $("#avatar-input").val()
    $.get('/profile/' , {profile_image}).then(response => {
        if (response.status === 'successful'){
            // Swal.fire({
            //       title: 'Profile Picture Changed !',
            //       icon: 'success',
            //       confirmButtonColor: '#3085d6',
            //       confirmButtonText: 'OK!'
            //     })
            setTimeout(()=>{location.reload()} , 2500)
        }
    })
}


function showresult() {
    var text = $("#searchproducts").val()
    if (text === ''){
        return
    }
    $.get('/show-result/' , {text}).then(response => {
        if (response.status === 'one'){
            location.href = '/product/'+ response.slug
        }else if (response.status === 'more'){
            $(".select-category").html(response.product_html)
        }
    })
}


function Filter(value , category) {
    var filter_type = value.filter_type
    console.log(value)
    $.get('/category/'+category , {'filter_type':value}).then(response => {
        $("#main-main").html(response)
        if (value === 'most_e'){
            $("#most").addClass('filter-active')
            $("#ch").removeClass('filter-active-c')
            $("#hi").removeClass('filter-active')
        }else if (value === 'cheapest'){
            $("#most").removeClass('filter-active')
            $("#ch").addClass('filter-active-c')
            $("#hi").removeClass('filter-active')
        }else if (value === 'highest_s'){
            $("#most").removeClass('filter-active')
            $("#ch").removeClass('filter-active-c')
            $("#hi").addClass('filter-active')
        }
    })

}



function AddComment(product_id) {
    var text = $("#comment-textinput").val()
    $.get('/add-comment/' , {text , product_id}).then( response=>{
        if (response.status === 'successful'){
            $("#main-com").html(response.html_code)
            $("#comment-textinput").val('')
            $("#com-count").html(response.count)
            document.getElementById('scroll-title').scrollIntoView({behavior:"smooth"})

        }
    })
}