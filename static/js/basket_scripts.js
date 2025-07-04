window.onload = function () {
    $('.basket_list').on('input', 'input[type="number"]', function (event) {
        const target = event.target;
        const nights = target.value;
        const pk = target.name;

        if (nights < 1) return;

        $.ajax({
            url: `/basket/edit/${pk}/${nights}/`,
            method: 'GET',
            success: function (data) {
                $('.basket_list').html(data.result);
                console.log('AJAX обновление выполнено');
            },
            error: function () {
                console.log('Ошибка обновления корзины');
            }
        });
    });
};