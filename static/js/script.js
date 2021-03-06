$(document).ready(function(){

	var first_name = $('#first_name_form');
	var last_name = $('#last_name_form');
    var email = $('#email_form');
    var feedback_name = $('#feedback_name_form');
    var feedback_email = $('#feedback_email_form');
    var feedback_message = $('#message_form')


	// проверка ввода обязательных полей
	function validator(obj, event=undefined){
		let reg = /^[а-я]+$/i;  // регулярное выражение, только кириллица, больше одного символа

		if (!reg.test(obj.val())) {
			obj.addClass("is-invalid");
			$('.invalid-feedback').text("Некорректные данные")
			if (event != undefined){
				event.preventDefault() // останавливает отправку данных на сервер
			}
		} else {
			obj.removeClass("is-invalid");
			obj.addClass("is-valid");
		};
	};

	// проверка введенного email на соответствие шаблона
	function email_validator(email, event=undefined) {
		let reg = /^[a-z0-9_-]+@[a-z]+\.[a-z]{2,6}$/i;  // adress@example.com

		if (!reg.test(email.val())) {
			email.addClass("is-invalid");
			$('#error-email').text("Некорректный email!")
			event.preventDefault();
		} else {
			email.removeClass('is-invalid');
			email.addClass('is-valid');
		};
	};

	// валидация полей при изменении
	first_name.blur(function (event) {validator($(this))});
	last_name.blur(function (event) {validator($(this))});
    email.blur(function (event) {email_validator($(this))});

	// валидация регистрационных данных при отправке на сервер
	$('#registration-form').submit(function (event) {
		validator(first_name, event);
		validator(last_name, event);
		email_validator(email, event);
    });
	
	// валидация данных форм при изменении
    feedback_name.blur(function (event) {validator($(this))});
	// поле "Сообщение" не может быть пустым
	feedback_message.blur(function (event) {
        if ($(this).val() == '') {
            $(this).addClass("is-invalid");
            $('.invalid-feedback').text("Пустое сообщение!")
        } else {
			$(this).removeClass("is-invalid");
			$(this).addClass("is-valid");
		};
    });
	feedback_email.blur(function (event) {email_validator($(this))});


	// валидация данных обратной связи при отправке на сервер
    $('#feedback-form-container').submit(function(event) {
        validator(feedback_name, event);
		email_validator(feedback_email, event);
    });

});