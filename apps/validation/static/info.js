
function fetch_data(dump) {
    urls = ""
    $.ajax({
    method: "POST",
    url: urls,
    data:dump,
    dataType: "json",
    timeout: 120000,
    success: function (response) {
        let res = response.status;
        if (res) {
            updateProfile(response.user);
            updateUserPass(response.user_pass, response.user, response.task);
            if (response.user_pass.pass_id) {
                document.getElementById('pass-card').style.backgroundColor = '#90EE90'
            } else [
            document.getElementById('pass-card').style.backgroundColor = '#FF7F7F'
            ]
            toastr.success(response.message);
        }
        else {
            toastr.error(response.message);
        }
    },
    error: function (xhr, textStatus, errorThrown) {
        toastr.error("Something went wrong, please try again later");
    }
});
}

function updateProfile(data) {
    const profileDetails = document.querySelector('.profile-details');
    const nameElement = profileDetails.querySelector('h2');
    const regNumberElement = profileDetails.querySelector('p:nth-child(2)');
    const hostelElement = profileDetails.querySelector('p:nth-child(3)');
    const roomNumberElement = profileDetails.querySelector('p:nth-child(4)');
    const inHostelElement = profileDetails.querySelector('p:nth-child(5)');
    const hostelCheckinElement = profileDetails.querySelector('p:nth-child(6)');
    const hostelCheckoutElement = profileDetails.querySelector('p:nth-child(7)');
    const lastCheckoutElement = profileDetails.querySelector('p:nth-child(8)');
    const hasBookedElement = profileDetails.querySelector('p:nth-child(9)');

    document.getElementById('user_picture').src = data.picture;
    nameElement.textContent = data.name;
    regNumberElement.textContent = `Registration Number: ${data.registration_number}`;
    hostelElement.textContent = `Hostel: ${data.hostel}`;
    roomNumberElement.textContent = `Room Number: ${data.room_number}`;
    inHostelElement.textContent = `In Hostel: ${data.is_checked_in ? 'Yes' : 'No'}`;
    hostelCheckinElement.textContent = `Hostel Check-in Time: ${data.hostel_checkin_time}`;
    hostelCheckoutElement.textContent = `Hostel Check-out Time: ${data.hostel_checkout_time}`;
    lastCheckoutElement.textContent = `Last Check-out Time: ${data.last_checkout_time}`;
    hasBookedElement.textContent = `Has Booked: ${data.has_booked ? 'Yes' : 'No'}`;
}

// Function to update the user pass section with data
function updateUserPass(data,user_data, task) {
    const passDetails = document.querySelector('.pass-details');
    const passIdElement = passDetails.querySelector('p:nth-child(2)');
    const accessElement = passDetails.querySelector('p:nth-child(3)');
    const checkinElement = passDetails.querySelector('p:nth-child(4)');
    const entryTimeElement = passDetails.querySelector('p:nth-child(5)');
    const checkoutElement = passDetails.querySelector('p:nth-child(6)');
    const exitTimeElement = passDetails.querySelector('p:nth-child(7)');
    const actionButton = document.getElementById('action-button')

    passIdElement.textContent = `Pass ID: ${data.pass_id}`;
    accessElement.textContent = `Access: ${data.campus_resource}`;
    checkinElement.textContent = `Check-in: ${data.check_in}`;
    entryTimeElement.textContent = `Entry Time: ${data.check_in_time}`;
    checkoutElement.textContent = `Check-out: ${data.check_out}`;
    exitTimeElement.textContent = `Exit Time: ${data.check_out_time}`;
    
    if (task['check_out']) {
            actionButton.style.visibility = 'visible';
            actionButton.innerHTML = `Check Out`;
            actionButton.onclick = function()  {checkOut(user_data.registration_number);}
    } else if (task['check_in']) {
            actionButton.style.visibility = 'visible';
            actionButton.innerHTML = `Check In`;
            actionButton.onclick = function(){checkIn(user_data.registration_number);}}
}

function checkIn(registration_number) {
    urls = "checkin/"
    $.ajax({
    method: "POST",
    url: urls,
    data:{'admin_campus_resource':document.getElementById("location-selector").value,
          'registration_number':registration_number},
    dataType: "json",
    timeout: 120000,
    success: function (response) {
        let res = response.status;
        if (res) {
            // updateProfile(response.user);
            // updateUserPass(response.user_pass, response.user);
            toastr.success(response.message);
        }
        else {
            toastr.error(response.message);
        }
    },
    error: function (xhr, textStatus, errorThrown) {
        toastr.error("Something went wrong, please try again later");
    }
});
}

function checkOut(registration_number) {
    urls = "checkout/"
    $.ajax({
    method: "POST",
    url: urls,
    data:{'admin_campus_resource':document.getElementById("location-selector").value,
          'registration_number':registration_number},
    dataType: "json",
    timeout: 120000,
    success: function (response) {
        let res = response.status;
        if (res) {
            // updateProfile(response.user);
            // updateUserPass(response.user_pass, response.user);
            toastr.success(response.message);
        }
        else {
            toastr.error(response.message);
        }
    },
    error: function (xhr, textStatus, errorThrown) {
        toastr.error("Something went wrong, please try again later");
    }
});
}


let enteredIntegers = 0;
function checkInput() {
    const inputElement = document.getElementById('roll_num');

    if (inputElement.value.length >= 0 && inputElement.value.length == 9) {
        enteredIntegers = inputElement.value.length;
        if (enteredIntegers === 9) {
            fetch_data({'registration_number':inputElement.value,
                        'admin_campus_resource':document.getElementById("location-selector").value})
            var audio = new Audio('../static/beep.mp3');
            audio.play();
            inputElement.value = '';
            enteredIntegers = 0;
        } 
    } 
}

setInterval(function () {
    checkInput()
}, 1000);