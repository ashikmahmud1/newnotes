if (window.location.pathname == '/teachers/create') {
    $(function () {
        $('select[name=school]').change(function (e) {
            if ($('select[name=school]').val() == 'not-listed') {
                $('#new-school').show();
            } else {
                $('#new-school').hide();
            }
        });

    });

}