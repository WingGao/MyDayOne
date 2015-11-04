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

function load_entry_modal(dayonecard) {
    var card = $(dayonecard);
    var modal = $('#dayone-modal');
    modal.modal('show');
    //modal.find('.entry_img').attr('src',card.find())
    var img = card.find('.dayone-entry-img').css('background-image');
    modal.find('.modal-title').text(card.find('.dayone-date').attr('dayone-date'));
    modal.find('.entry_img').attr('src', img == undefined ? '' : img.substring(5, img.length - 2));
    modal.find('.dayone-entry-text').html(card.find('.mdl-card__supporting-text').html());

}

function nl2br(str, is_xhtml) {
    var breakTag = (is_xhtml || typeof is_xhtml === 'undefined') ? '<br ' + '/>' : '<br>';

    return (str + '')
        .replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1' + breakTag + '$2');
}