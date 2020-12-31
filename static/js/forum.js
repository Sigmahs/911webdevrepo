$(() => {
  
  const setHeight = () => { // set threads column height
    $('.thread-items').css('height', $(window).height() - $('.thread-head').height());
  }

  setHeight();
  $(window).resize(() => {
    setHeight();
  });

  function arrayUnique(value, index, self) { 
    return self.indexOf(value) === index;
}

  // return the pks of the comments of a given thread
  const getComments = (threadPk) => {
    var commentArray = [];
    $('.comment-description').each((idx, tag) => {
      const thisPk = $(tag).attr('data-thread-pk');
      if (thisPk == threadPk) {
        commentArray.push($(tag).attr('data-comment-pk'));
      }
    }); 
    return commentArray.filter(arrayUnique);
  };

  const numComments = (threadPk) => getComments(threadPk).length;

  // displays the comments of a given thread
  const showComments = (threadPk) => {
    console.log('showing comments');
    console.log(threadPk);
    const pkArray = getComments(threadPk);
    if (numComments(threadPk) == 0) {
      $(`.display-content[data-pk="${threadPk}"]`).find('.no-comments').toggleClass('hide');
    }
    console.log(numComments(threadPk));
    $('.comment-description').each((idx, tag) => {
      if (!$(tag).hasClass('hide')) {
        $(tag).addClass('hide');
      }
      if (pkArray.includes($(tag).attr('data-comment-pk'))) {
        if ($(tag).hasClass('hide')) {
          $(tag).removeClass('hide');
        }
      }
    });
  };

  $('.forum-container').each((idx, tag) => {
    console.log($(tag).find('.forum-title').first())
    const width = $(tag).find('.forum-title').first().width();
    $(tag).find('.fix-width').first().css('width', width);

    const threadPk = $(tag).attr('data-pk');
    const number = numComments(threadPk);
    $(tag).find('.comment-count').first().html(`Comments: ${number}`);
  });

  // display a thread's content on click
	$('.forum-container').each((idx, container) => {
		$(container).on('click', (e) => {
			$('.forum-container').each((idx, container2) => { // return to default
        const number = getNumber(container2);
				$('#forum-number-' + number).css('background-color', '#16254C');
        if (!$('#forum-number-' + number).find('.arrow-left').hasClass('hide')) {
          $('#forum-number-' + number).find('.arrow-left').addClass('hide');
        }
        if (!$('#content-no-' + number).hasClass('hide')) {
          $('#content-no-' + number).addClass('hide');
        }
        if (!$('.waiting-text').hasClass('hide')) {
          $('.waiting-text').addClass('hide');
        }
			});
      const number = getNumber(container);
			$(e.target).closest('.forum-container').css('background-color', '#425390');
      if ($(e.target).closest('.forum-container').find('.arrow-left').hasClass('hide')) {
        $(e.target).closest('.forum-container').find('.arrow-left').removeClass('hide');
      }
      if ($('#content-no-' + number).hasClass('hide')) {
        $('#content-no-' + number).removeClass('hide');
      }
      console.log('data pk below');
      console.log('#content-no-' + number);
      console.log($('#content-no-' + number));
      console.log($('#content-no-' + number).attr('data-pk'));
      showComments($('#content-no-' + number).attr('data-pk'));

      // delete thread
      const pk = getPK(container);
      $(`#${pk}.delete-thread`).on('click', () => {
        var pk = $(this).attr('pk');
        $.ajax({
          url:  `http://localhost:8000/delete_thread/${pk}/`,
          data: { 'id' : pk },
          beforeSend: xhr => function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}" );
          },
          success: response => {
            $(`.forum-container[data-pk="${pk}"]`).closest('.thread').slideUp();
          }
        });
      });
		});
	});

  // get thread Number
  const getNumber = container => {
    const numberString = $(container).closest('.forum-container').attr('id');
    const number = numberString.substring(13, numberString.length);
    return number;
  };

  // get thread Primary Key
  const getPK = container => {
    return pk = $(container).find('.forum-container').attr('data-pk');
  };

  // show thread form on click
  $('.add-thread').on('click', (event) => {
    $('.add-thread').css({'color': '#D3D3D3', 'cursor': 'auto'});
    if ($('.thread-form').hasClass('hide')) {
      $('.thread-form').removeClass('hide');
    }
  });

  // show comment form on click
  $('.reply-thread').on('click', (event) => {
    $('.comment-form').toggleClass('hide');
  });

});