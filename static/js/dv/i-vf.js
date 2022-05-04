const input = document.querySelector("#phone");

const iti = window.intlTelInput(input, {
    utilsScript: "{{ url_for('static', filename='phone/phone_build/js/utils.js?1638200991544') }}"
});

function coptyToClipboard(e) {
    const $temp = $("<input>");
    $("body").append($temp);
    $temp.val($(e).text()).select();
    document.execCommand("copy");
    $temp.remove();
}


iti.promise.then(function() {
    setInterval(()=> {
        $("#loader").hide();
        $("#form").show();
    }, 1000)
});

const csrf_token = "{{ csrf_token() }}";

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});


jQuery.validator.addMethod("phoneNumValidation", function(value) {
    return iti.isValidNumber();
}, 'Please enter a valid number');

jQuery.validator.addMethod("onlyNumber", function(value) {
    const pattern = /^\d+$/;
    return pattern.test(value);
}, 'Please enter a valid number');

const validator = $("#form").validate({
    onkeyup: function(element) {
        this.element(element);
    },
    onclick: function(element) {
        this.element(element);
    },
    onfocusout: function(element) {
        this.element(element);
    },
    rules: {
        ph_num: {
            required: true, 
            phoneNumValidation: true,
            onlyNumber: true
        },
        verify_code: {
            required: true,
            onlyNumber: true,
            minlength: 6,
            maxlength: 6,
        }

    },
    messages: {
        ph_num: {
            required: "Pls Enter your contact Number",
        },
        verify_code: {
            required: "Pls Enter your verify code"
        }
    },
    errorClass: 'invalid-field',
    errorPlacement:
    function( error, element ){

        if (element[0].parentElement.getAttribute("id") == 'ph-vfc') {

            console.log('catch');

            element[0].nextElementSibling.textContent = error.text();
            
        }
        else {
            element[0].parentElement.nextElementSibling.textContent = error.text();
        }

    },
    success: function(error, element) {

    }
});

$("#form input, #form select").on('change', function() {
    validator.form();
});

$("#step-send").on('click', function(e) {
    e.preventDefault();
    validator.form();

    let validation = $("#form").valid();

    if (validation === true) {
        $(".ov-lay").show();
        $(".op-4").css('opacity', 0.4);
        setTimeout(() => {
            $(".op-4").css('opacity', 1);
            let d = document.createElement("div");
            d.setAttribute('id', 'ph-vfc');
            d.classList.add("mb-4");
            let i = document.createElement("input");
            i.name = "verify_code";
            i.placeholder = "Enter Verify Code";
            i.classList.add("form-control");
            i.classList.add("mx-150");
            let inv_div = document.createElement("div");
            inv_div.classList.add("invalid-feedback");
            d.appendChild(i);
            d.appendChild(inv_div);
            $(d).insertAfter($("#ph-sc"));
            let sv = $("#step-send").clone().prop('id', 'step-verify');
            sv.val("Verify code")
            $(sv).insertAfter($("#step-send"));
            $("#phone")[0].setAttribute('readonly', true);
            sv_pd();
            $("#step-send").remove();
            $(".ov-lay").hide();
        }, 3000)
    }
});

function convertFormToJSON(form) {
    return $(form)
        .serializeArray()
        .reduce(function (json, { name, value }) {
        if (name == "ph_num") {
            value = iti.activeItem.childNodes[2].innerText + value;
        }
        json[name] = value;
        return json;
        }, {});
}

function sv_pd() 
{
    $("#step-verify").on('click', function(e) {
        e.preventDefault();
        validator.form();

        let validation = $("#form").valid();

        if (validation === true) {
            $(".ov-lay").show();
            $(".op-4").css('opacity', 0.4);
            $.ajax("/info/verify", {
                type: "POST",
                contentType: 'application/json;charset=UTF-8',
                data: JSON.stringify({
                    "ph_num": iti.activeItem.childNodes[2].innerText + $("input[name='ph_num']").val(),
                    'verify_code': $("input[name='verify_code']").val(),
                }),
                success: function(data, status, xhr) {
                    $(".ov-lay").hide();
                    $(".op-4").css('opacity', 1);
                    let vf = data["valid"];

                    if (vf === true) {

                        const vf_input = document.querySelector("input[name='verify_code']");
                        vf_input.classList.remove('border-danger');

                        let d = document.createElement("div");
                        d.classList.add("fn-lay")
                        let img = document.createElement("img");
                        img.src="{{ url_for('static', filename='check.svg') }}";
                        img.classList.add("success");
                        img.alt = "Success";
                        let t = document.createElement("h4");
                        t.classList.add("lead")
                        t.classList.add("text-center")
                        t.innerText = "All your information are correct, and you'r ready to send.";
                        d.append(img);
                        d.append(t);
                        $(d).insertBefore($("#form .ov-lay"));

                        let quote = $("#step-verify").clone().prop('id', 'step-quote');
                        quote.val("Send quote");
                        $(quote).insertAfter($("#step-verify"));
                        $("#step-verify").remove();
                        send();

                    }
                    else 
                    {
                        let error = document.createElement("span");
                        error.textContent = "Invalid Code!";
                        const vf_input = document.querySelector("input[name='verify_code']");
                        vf_input.classList.add('border-danger');
                        vf_input.nextSibling.appendChild(error);
                    }
                },  
                error: function(jqXhr, textStatus, errorMessage) {
                    console.log(errorMessage);
                }
            })
        }

    });
}

function send() {
    $("#step-quote").on('click', function(e) {
        e.preventDefault();
        validator.form();
        $.ajax("/store/quote", {
            type: "POST",
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify(convertFormToJSON("#form")),
            success: function(data, status, xhr) {
                if (data.valid === true && data.status === true) {
                    return window.location = "{{ url_for('.quoted', _external=True) }}" + `?name=${data.name}`;
                }
                else {
                    $("#sh-error").html(data.msg);
                    $("#step-quote")[0].setAttribute('disabled', true);

                    setTimeout(() => {
                        return window.location = "{{ url_for('.index', _external=True) }}";
                    }, 4000);

                }
            },
            error: function(jqXhr, textStatus, errorMessage) {
            }
        })
    });
}