var fileSizePattern = /^(\d+(?:\.\d+)*)\s*([egkmpt])b?$/i;

$(document).ready(function() {
        // Initialize the jQuery File Upload widget:
	var number_id = 0
        $('#fileupload').fileupload({maxNumberOfFiles: downloader.constants.MAX_NUMBER_OF_FILES,
				     maxFileSize: downloader.constants.MAX_FILE_UPLOAD_SIZE})
                .bind('fileuploaddone', function (e, data) {
		    $('<input />', {type: 'hidden',
				    id: '#id_file_id_'+number_id,
				    name: 'file_id',
				    value: data.result[0].file_id}).appendTo("#upload_form")
		    number_id++;
		});

        // Load existing files:
        $.getJSON($('#fileupload form').prop('action'), function (files) {
            var fu = $('#fileupload').data('fileupload');
            fu._adjustMaxNumberOfFiles(-files.length);
            fu._renderDownload(files)
                .appendTo($('#fileupload .files'))
                .fadeIn(function () {
                    // Fix for IE7 and lower:
                    $(this).show();
                });
        });

        // Open download dialogs via iframes,
        // to prevent aborting current uploads:
        $('#fileupload .files a:not([target^=_blank])').live('click', function (e) {
            e.preventDefault();
            $('<iframe style="display:none;"></iframe>')
                .prop('src', this.href)
                .appendTo('body');
        });

    /*
            onComplete: function( id, fileName, responseJSON ) {
                if( responseJSON.success ) {
                    $("#id_file_id").val(responseJSON.file_id);
                    $("#progress_bar").hide('slow');
          });*/
    });
