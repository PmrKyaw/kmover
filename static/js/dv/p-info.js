jQuery.validator.addMethod("notInPast", 
function(value, element) {

    var d = new Date(),
    month = '' + (d.getMonth() + 1),
    day = '' + d.getDate(),
    year = d.getFullYear();
    
    if (month.length < 2) 
    {
        month = '0' + month;
    }
    if (day.length < 2) 
    {
        day = '0' + day;
    }
    
    let cp = [year, month, day].join('-');


    return this.optional(element) || (cp < value);

    
},'Date can\'t be in past.');

jQuery.validator.addMethod("emailExt", function(value, element, param) {
    return value.match(/^[a-zA-Z0-9_\.%\+\-]+@[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,}$/);
},'Email is invalid!');

const validator = $("#form").validate({
    onkeyup: function(element) {
        this.element(element);  

    },
    onclick: function(element) {
        this.element(element);
    },
    onfocusout: function(element) {
        if (element.classList.contains('date-control') & 
        element.getAttribute('uids') === '0') {
            element.setAttribute('uids', '1');

        }
        else {
            this.element(element);
        }

    },
    rules: {
        salutation: {
          required: true
        },
        name: {
            required: true, 
            minlength: 4,
            maxlength: 20
        },
        email: {
            required: true,
            emailExt: true
        },
        est_move_date: {
            required: true,
            date: true,
            notInPast: true

        },
        msg: {
            maxlength: 200
        }

    },
    messages: {
        salutation: {
            required: "Enter a Given Salutation or Gender"
        },
        name: {
            required: "Enter your Name",
            minlength: "Name need to be at least 4 character",
            maxlength: "Name need to be less than 20 character",

        },
        email: {
            required: "Enter email"
        },
        est_move_date: {
            required: "Esitmated move date can't be empty!",
            date: "Invalid date"
        }
    },
    errorClass: 'invalid-field',
    errorPlacement:
    function( error, element ){

        if (element.first().hasClass('date-control')) {

            element[0].nextElementSibling.nextElementSibling.textContent = error.text();


            if (element[0].getAttribute('uids') !== '0') {
            }
            
        }
        else {
            element[0].nextElementSibling.textContent = error.text();
        }

    },
    success: function(error, element) {

    }
});

$("#form input, #form select").on('change', function() {
    validator.form();
});


$("#datepicker").datepicker({
    autoclose: true,
    format: 'yyyy-mm-dd'
}).on("changeDate", function(e) {
    // e.currentTarget.children[0].setAttribute('uids', '1');
    validator.form();
}).on('hide', function(ev) { // <-----------
    validator.form();
});;

$( "#datepicker" ).datepicker( "setDate", '2022-06-02');



