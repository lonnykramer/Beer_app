//CheckBoxes Single Choice at a time
$('.radiocheck').on('change', function () {
  $('.radiocheck').not(this).prop('checked', false);
});

$('.ibu').on('change', function () {
  $('.ibu').not(this).prop('checked', false);
});

$('.alevel').on('change', function () {
  $('.alevel').not(this).prop('checked', false);
});

$('.mfeel').on('change', function () {
  $('.mfeel').not(this).prop('checked', false);
});

$('.color').on('change', function () {
  $('.color').not(this).prop('checked', false);
});

// Submit Button


