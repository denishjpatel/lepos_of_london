$(document).ready(function() {

    $('.razorpay').click(function(e) {
        if ($('#first_name').val().length == 0){
            alert("Please fill first name!");
            return false;
        } else if ($('#last_name').val().length == 0){
            alert("Please fill last name!");
            return false;
        } else if ($('#exampleInputEmail1').val().length == 0){
            alert("Please fill email!");
            return false;
        } else if ($('#contact_number').val().length == 0){
            alert("Please fill contact number!");
            return false;
        } else if ($('#address').val().length == 0){
            alert("Please fill address!");
            return false;
        } else if ($('#city').val().length == 0){
            alert("Please fill city!");
            return false;
        } else if ($('#pincode').val().length == 0){
            alert("Please fill pincode!");
            return false;
        } else if ($('#state').val().length == 0){
            alert("Please fill state!");
            return false;
        } else if ($('#country').val().length == 0){
            alert("Please fill country!");
            return false;
        }

        if ($('#exampleCheck1').is(':checked')) {
            
            // return true;

            e.preventDefault();

            var first_name = $("[name='first_name']").val();
            var last_name = $("[name='last_name']").val();
            var total_price = 1;
            // var total_price = $("[name='total_price']").val();
            var sub_total = $("[name='sub_total']").val();
            var address = $("[name='address']").val();
            var city = $("[name='city']").val();
            var pincode = $("[name='pincode']").val();
            var state = $("[name='state']").val();
            var country = $("[name='country']").val();
            var contact_number = $("[name='contact_number']").val();
            var email = $("[name='email']").val();
            var csrfmiddlewaretoken = $("[name='csrfmiddlewaretoken']").val();
            var order_id = $("[name='order_id']").val();
            var ids = $("input[id='ids']").map(function() { return $(this).val(); }).get();
            var qtys = $("input[id='qty']").map(function() { return $(this).val(); }).get();
            // var unit_prices = 1;
            var unit_prices = $("input[id='unite_price']").map(function() { return $(this).val(); }).get();
            console.log("Get it");
            console.log(order_id);
            var options = {
                "key": "rzp_test_T15HUukxUCbpYR", // Enter the Key ID generated from the Dashboard
                "amount": (total_price * 100), // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                "currency": "INR",
                "name": "Ecommerce Site",
                "description": "Thank You",
                "image": "https://example.com/your_logo",
                // "order_id": order_id, //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                "handler": function(response) {
                    console.log(response);
                    // alert(response.razorpay_payment_id);
                    // alert(response.razorpay_order_id);
                    // alert(response.razorpay_signature)
                    data = {
                            "first_name": first_name,
                            "last_name": last_name,
                            "total_price": total_price,
                            "address": address,
                            "email": email,
                            "razorpay_payment_id": response.razorpay_payment_id,
                            csrfmiddlewaretoken: csrfmiddlewaretoken,
                            "payment_mode": "Razorpay",
                            "sub_total": sub_total,
                            "city": city,
                            "pincode": pincode,
                            "state": state,
                            "country": country,
                            "contact_number": contact_number,
                            "ids": ids,
                            "qtys": qtys,
                            "unit_prices": unit_prices,
                            "order_id": order_id,
                        },
                        $.ajax({
                            method: "POST",
                            url: "/order/order-with-razorpay/",
                            data: data,
                            success: function(result) {
                                window.location.href = 'my-orders/'
                            }
                        })
                },

                "prefill": {
                    "name": first_name + " " + last_name,
                    "email": email,
                    "contact": contact_number
                },
                "notes": {
                    "address": "Razorpay Corporate Office"
                },
                "theme": {
                    "color": "#3399cc"
                }
            };
            console.log("1");
            var rzp1 = new Razorpay(options);
            console.log("2");
            rzp1.open();
            console.log("3");
        } else {
            alert("Oops! You haven't agreed terms and conditions!");
            return false;
        }
    });

});