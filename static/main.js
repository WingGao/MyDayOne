var _local_entry_cache = {};

function load_entry(uuid) {
    console.log(uuid);
    $('#entry_spinner').show();
    var success = function (d) {
        $('#entry_spinner').hide();
        $('#entry_text').html(nl2br(d.text));
        if (d.image) {
            $('#entry_img').attr('src', '/photo/' + d.uuid);
        } else {
            $('#entry_img').attr('src', '');
        }

    };
    if (_local_entry_cache.hasOwnProperty(uuid))
        success(_local_entry_cache[uuid]);
    else
        $.getJSON('/entry/' + uuid + '?format=json', function (d) {
            _local_entry_cache[uuid] = d;
            success(d);
        })
}

function nl2br(str, is_xhtml) {
    var breakTag = (is_xhtml || typeof is_xhtml === 'undefined') ? '<br ' + '/>' : '<br>';

    return (str + '')
        .replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1' + breakTag + '$2');
}