$(document).ready(function(){
	var year = $('#year'),
		kcdng = $('#kcdng_rul'),
		kip_mas = $('#kip_mas'),
		asup = $('#kcdng_asup'),
		month = $('#month'),
		new_year = $('.new_year'),
		new_month = $('.new_month'),
		new_mas = $('#new_mas'),
		new_kcdng = $('#new_kcdng'),
		new_kcdngs = $('#new_kcdngs'),
		new_perkkcdng = $('#new_perkkcdng'),
		new_perkkcdngs = $('#new_perkkcdngs'),
		new_asup = $('#new_asup'),
		pre_month = $('#pre_month');
		year.on('change',function () {

			var updateresult = function () {
				new_year.text(year.val());
			}
			updateresult();
				
		});
		month.on('change',function () {

			var updateresult = function () {
				new_month.text(month.val());
				if (month.val()=='01') {
					pre_month.text('12')
				}else{
					if (parseInt(month.val())<11) {
						pre_month.text('0'+(parseInt(month.val())-1));
					} else {
						pre_month.text(parseInt(month.val())-1);	
						
					};
					
				};
				console.log(month.val());
				console.log(parseInt(month.val()));
			}
			updateresult();
				
		});
		kip_mas.on('change',function () {

			var updateresult = function () {
				new_mas.text(kip_mas.val());
			}
			updateresult();
				
		});
		asup.on('change',function () {

			var updateresult = function () {
				new_asup.text(asup.val());
			}
			updateresult();
				
		});
		kcdng.on('change',function () {

			var updateresult = function () {
				if (kcdng.val()=='1') {
					new_kcdng.text('Болсун С.А.');
					new_kcdngs.text('Болсуна С.А.');
					new_perkkcdng.text('Начальник');
					new_perkkcdngs.text('Начальника');
				} else {
					new_kcdng.text('Тодесеев С.В.');
					new_kcdngs.text('Тодесеева С.В.');
					new_perkkcdng.text('Заместитель начальника');
					new_perkkcdngs.text('Заместителя начальника');
				}
				
			}
			updateresult();
				
		});
		
});