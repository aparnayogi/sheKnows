function register_login_events(){

    $(document).on("click", "#loginSubmit", function(e){
        var userName = $("#userLoginEmail").val();
        var password = $("#userLoginPassword").val();
        var request_data = {
            "user_email": userName,
            "password":password
        }
        console.log(request_data)
        verify_user_login(request_data);
    }); 

    $(document).on("click", "#registrationSubmit", function(e){
   
        var firstName = $("#userFirstName").val();
        var lastName = $("#userLastName").val();
        var mobile = $("#userMobileNo").val();
        var email = $("#userEmail").val();
        var password = $("#userPassword").val();
        var city = $("#userCity").val();
        
        var password = $("#userPassword").val();
    
        var request_data = {
            "first_name" : firstName,
            "last_name" : lastName,
            "email":email,
            "mobile_no":parseInt(mobile),
            "password": password,
            "city":city,
            
       }
        
        
        console.log(request_data)
        user_signup(request_data);
    });





}


function user_signup(request_data){
   
    $.ajax({
        url:'/user_signup',
        type:"POST",
        dataType:"json",
        contentType : "application/json",
        data : JSON.stringify(request_data),
        beforeSend : function() {
            
        },
        success : function (data, status, xhr){
           
        },
        error : function(jqXhr, textStatus, errorMsg){
            console.log(errorMsg);
        }
    });
}

function verify_user_login(request_data){
    
    $.ajax({
        url:'/attempt_to_login',
        type:"POST",
        dataType:"json",
        contentType : "application/json",
        data : JSON.stringify(request_data),
        beforeSend : function() {
        },
        success : function (data, status, xhr){
            console.log(data)
            if(data['status'] == 'Login Successful'){
                console.log("Login done");
                window.location.href = '/home';
            }
            else{
                window.location.href = '/login';
            }
        },
        error : function(jqXhr, textStatus, errorMsg){
            console.log(errorMsg);
        }
    });
}

