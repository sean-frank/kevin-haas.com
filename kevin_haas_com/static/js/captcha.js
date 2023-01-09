function captchas() {
	$(document).ready(function() {
		'use strict';
		
		$(this.head).append([
			$('<link>').attr('rel', 'stylesheet').attr('href', '/static/css/captcha.css'),
		]);
		
		function genCaptcha(totalChars) {
			const alphaNums = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
			const chars = Array.from(Array(totalChars), (a, i) => alphaNums[Math.floor(Math.random() * alphaNums.length)]);
			return chars.join('');
		}
		
		function setCanvasText(canvas, text) {
			canvas.each(function() {
				let ctx = this.getContext("2d");
				ctx.clearRect(0, 0, this.width, this.height);
				ctx.fillText(text, this.width / 4, this.height / 2);
			});
			return;
		}
		
		$('form').each(function() {
			'use strict';
			
			let form = $(this);
			
			let captchaValid = false;
			let captchaWrap = $('<div>').addClass('captcha').html([
				'<h3>Simple Captcha</h3>',
				'<canvas id="captcha"></canvas>',
				'<label for="captcha-input">Captcha: </label>',
				'<input type="text" name="text" id="captcha-input" autocomplete="off" />',
				'<button id="captcha-submit" type="button">Submit</button>',
				'<button id="captcha-refresh" type="button">Refresh</button>',
				'<div id="captcha-output" class=""></div>'
			]);
			
			form.prepend(captchaWrap);
			
			form.find('[type="submit"]').on('submit', function(e) {
				e.preventDefault();
				if (validateCaptcha()) {
					$(this).parents('form').first().submit();
				} else {
					window.alert('A valid captcha is required.');
				}
			});
			
			let captcha = form.find('#captcha');
			let userText = form.find('#captcha-input');
			let submitButton = form.find('#captcha-submit');
			let output = form.find('#captcha-output');
			let refreshButton = form.find('#captcha-refresh');
			
			captcha.each(function() {
				let ctx = this.getContext("2d");
				ctx.font = "15px 'Courier New'";
			});
			
			var rngCaptcha = genCaptcha(7);
			setCanvasText(captcha, rngCaptcha);
			
			submitButton.on('click', function(e) {
				captchaValid = userText.val() === rngCaptcha;
				
				if (captchaValid) {
					output.addClass("captcha-correct").removeClass("captcha-incorrect");
					output.text("Correct!");
				} else {
					output.addClass("captcha-incorrect").removeClass("captcha-correct");
					output.text("Incorrect, please try again...");
				}
			});
			
			userText.on('keyup', function(e) {
				// Key Code Value of "Enter" Button is 13
				if (e.keyCode === 13) {
					submitButton.click();
				}
			});
			
			refreshButton.on('click', function(e) {
				rngCaptcha = genCaptcha(7);
				setCanvasText(captcha, rngCaptcha);
				userText.val('');
				output.html('');
			});
			
			form.on('captchaEvent', function(e) {
				console.log('captchaEvent');
				if (captchaValid) {
					$(this).trigger('submit');
				}
			});
			
			form.find('button[type="submit"]').on('click', function(e) {
				e.preventDefault();
				console.log('invoking captchaEvent');
				form.trigger('captchaEvent');
			});
		});
	});
	return;
}