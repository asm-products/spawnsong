(function (spawnsong) {
  "use strict";
  
  ////
  // Orders
  ////

  function SnippetOrders(el) {
    this.orderEl = el;
    this.stripePublicKeys = window.STRIPE_PUBLIC_KEY; // set in base.html
    this.price = window.SONGSPAWN_SNIPPET_DETAILS.price;
    this.title = window.SONGSPAWN_SNIPPET_DETAILS.title;
    this.userEmail = window.LOGGED_IN_USER_EMAIL;
    this.snippetId = window.SONGSPAWN_SNIPPET_DETAILS.id;

    var _this = this;
    this.handler = window.StripeCheckout.configure({
      key: this.stripePublicKeys,
      token: function(token, args) {
        _this.orderEl.attr('disabled', true);
        _this.orderEl.text("Processing...");
        $('#orderForm [name=email]').val(token.email);
        $('#orderForm [name=token]').val(token.id);
        $('#orderForm').submit();
        // Use the token to create the charge with a server-side script.
      }
    });

    this.showCheckout = _.throttle(this.showCheckout, 5000, {trailing: false});
  }

  SnippetOrders.prototype = {
    ready: function () {
      this.orderEl.click(_.bind(this.showCheckout, this));
    },
    showCheckout: function () {
      var _this = this;

      this.handler.open({
        name: 'Spawnsong',
        description: 'Pre Order "' + this.title + '"',
        email: this.userEmail,
        amount: this.price
      });
    }
  };

  function LoginToOrder(el) {
      this.orderEl = el;
  }
  LoginToOrder.prototype = {
    ready: function () {
      this.orderEl.click(_.bind(this.goToLogin, this));
    },
    goToLogin: function () {
      window.location = this.orderEl.attr('data-location');
    }
  };

  ////
  // Player
  ////
  
  function SnippetPlayer(el) {
    this.beatLocations = window.SONGSPAWN_SNIPPET_DETAILS.beats;
    this.visualisation = window.SONGSPAWN_SNIPPET_DETAILS.visualisation_effect;
  }

  SnippetPlayer.prototype = {
    ready: function () {
      this.setupMediaElementPlayer();
    },
    setupMediaElementPlayer: function ( ) {
      var _this = this;
      var repeatTimes = 0;
      
      $('audio').mediaelementplayer({
        videoHeight: 0,
        features: ['playpause','progress','current','duration', 'volume'],
        success: function (mediaElement, domObject) { 

          $('#player-repeat').click(function (e) {
            repeatTimes = parseInt(prompt("How many times do you want to repeat?", 1),10) || 1;
            mediaElement.play();
          });

          $('#player-waveform').click(function (e) {
            var parentOffset = $(this).parent().offset(); 
            var relX = e.pageX - parentOffset.left;
            mediaElement.setCurrentTime((relX / $('#player-waveform').width()) * mediaElement.duration);
            mediaElement.play();
          });
          
          mediaElement.addEventListener('timeupdate', function(e) {
            var position = (mediaElement.currentTime/mediaElement.duration) * $('#player-waveform').width();
            $('#player-progress').css('left', position + "px");
          });
          
          mediaElement.addEventListener('playing', function(e) {
            $('#playButtonOverlay').fadeOut();
            if (_this.visualisation === "pulsate") {
              _this.runVisualisation(mediaElement);
            }
          });

          mediaElement.addEventListener('ended', function(e) {
            repeatTimes--;
            if (repeatTimes > 0) {
              mediaElement.setCurrentTime(0);
              mediaElement.play();
            }
          });

          mediaElement.addEventListener('pause', function(e) {
            // repeatTimes = 0;
          });

          $('#playerImageContainer').click(function () {
            if (mediaElement.paused || mediaElement.ended) {
              mediaElement.play();
            } else {
              mediaElement.pause();
            }
          });
        },
      });
    },

    runVisualisation: function (mediaElement) {
      var _this = this;
      var beats = _.clone(this.beatLocations);
      function update() {
        var beat;
        if (mediaElement.paused || mediaElement.ended) return;
        while(beats[0] < mediaElement.currentTime) {
          beat = beats.shift();
        }
        // 0.1 seconds before the beat we add the class, the
        // css transition time is set to 0.1 so it will reach its peak at
        // the same time as the beat.
        if (beats[0] && beats[0]-mediaElement.currentTime < 0.1) {
          $('#playerImage').addClass('beat');
        } else {
          $('#playerImage').removeClass('beat');
        }
        window.requestAnimationFrame(update);
      }
      // _.defer(update);
      window.requestAnimationFrame(update);
    }
  };

  ////
  // Comments
  ////
  
  function SnippetComments(el) {
  }

  SnippetComments.prototype = {
    ready: function () {
      $('#addcomment').click(_.bind(this.postComment, this));
    },

    /////
    // Comments
    ////
    
    // AJAXify the comment posting (progressively enhanced)
    postComment: function () {
      var text = $('#commentText').val().trim();
      if (text === '') return;
      var csrf = $('input[name=csrfmiddlewaretoken]').val();
      $('#addcomment').attr('disabled','disabled');
      $.ajax(document.location.href, {
        data: {comment: text, badger: ''},
        type: 'POST',
        headers: {'X-CSRFToken': csrf},
        success: function (data) {
          $('#comments').replaceWith($('#comments', data));
        }
      });
    },
  };
    

  ////
  // CSS Fixes
  ////
  
  // function SnippetViewCSS(el) {
  // }

  // SnippetViewCSS.prototype = {
  //   ready: function () {
  //     var _this = this;
  //     setInterval(function () {
  //       _this.setHeights();
  //     }, 500);
  //     this.setHeights();
  //   },
  //   // Fix up the heights of the page alements after page load
  //   setHeights: function () {
  //     var playerHeight = $('#playerContainer').height();
  //     $('#detailsContainer').css({height: playerHeight + 'px'});
  //     if ($('#comments ul').length) {
  //       $('#comments ul').css({height: playerHeight-$('#comments ul').position().top-50});
  //     }
  //   },

  // };
  
  /////
  // Uploads (used for both snippet and full song upload)
  ////
  
  function UploadForm(el) {
  }

  UploadForm.prototype = {
    ready: function () {
      if (!(new XMLHttpRequest().upload)) {
        // Browser doesn't support XHR2, fall back to standard HTML form
        return;
      }
      $('#uploadForm').ajaxForm({
        dataType: 'json',
        data: {xhr: true},
        beforeSubmit: function (arr, $form, option) {
          $('#uploadStatus').fadeIn();
          $('#uploadForm button').attr('disabled', true);
          // Disabling the inputs here breaks jquery.form, so disable
          // them in a ms
          setTimeout(function () {
            $('#uploadForm :input').attr('disabled', true);
          }, 1);
          // TOOD: Check file type
        },
        uploadProgress: function (evt, position, total, percentComplete) {
          $('#uploadStatus .progress-bar')
            .attr('aria-valuenow',percentComplete)
            .css({width: percentComplete + '%'})
            .find('.sr-only').text(percentComplete + '% complete');
          if (percentComplete > 99.99) {
            // Once we get to 100% upload it might still take a while
            // on the server, so add animated stripes to the progress
            // bar so that the user doesn't think it has stalled
            $('#uploadStatus .progress').addClass('progress-striped').addClass('active');
          }
        },
        error: function () {
          alert("Upload failed!");
        },
        success: function (response) {
          if (response.redirectTo) {
            document.location.href = response.redirectTo;
          } else {
            $('#uploadForm').html($('#uploadForm', response.html).html());
          }
        }
      });
    }
  };

  ////
  // Full song player
  ////
  
  function PersonalPlaylist(el) {
  }

  PersonalPlaylist.prototype = {
    ready: function () {
      var _this = this;
      this.setupMediaElementPlayer();
      $.endlessPaginate({
        paginateOnScroll: true,
        onCompleted: function(data) {
          _this.setupMediaElementPlayer();
        } 
      });
    },
    setupMediaElementPlayer: function ( ) {
      var _this = this;
      var players = [];
      $('audio').each(function () {
        var audio = $(this);
        var song = $(this).closest('.song');
        audio.mediaelementplayer({
          videoHeight: 0,
          features: ['playpause','progress','current','duration', 'volume'],
          success: function (mediaElement, domObject) { 
            players.push(mediaElement);

            var waveform = song.find('.player-waveform');
            var progress = song.find('.player-progress');
            
            waveform.click(function (e) {
              var parentOffset = $(this).parent().offset(); 
              var relX = e.pageX - parentOffset.left;
              mediaElement.setCurrentTime((relX / waveform.width()) * mediaElement.duration);
              mediaElement.play();
            });
            
            mediaElement.addEventListener('timeupdate', function(e) {
              var position = (mediaElement.currentTime/mediaElement.duration) * waveform.width();
              progress.css('left', position + "px");
            });
            
            
            mediaElement.addEventListener('ended', function(e) {
              var foundMe = false;
              var nextPlayer = _.find(players, function (player) {
                if (player === mediaElement) {
                  foundMe = true;
                } else {
                  return foundMe;
                }
              });
              if (nextPlayer) nextPlayer.play();
            });
          },
        });
      });
    }
  };

  ////
  // frontpage
  //
  
  function SnippetList(el) {
  }

  SnippetList.prototype = {
    ready: function () {
      $.endlessPaginate({
        paginateOnScroll: true,
      });
    }
  };

  var views = {
    '#order': SnippetOrders,
    '#loginToOrder': LoginToOrder,
    '#playerContainer': SnippetPlayer,
    '#personalPlaylistView': PersonalPlaylist,
    '#comments': SnippetComments,
    // '#snippetView': SnippetViewCSS,
    '#uploadForm': UploadForm,
    '#snippetList': SnippetList
  };

  function init() {
    for (var selector in views) {
      var el = $(selector);
      if (el.length && !el.data('sp-view')) {
        el.data('sp-view', new views[selector](el).ready(el));
      }
    }
  }

  $(document).ready(init);
  
  // InstantClick.init();
  // InstantClick.on('change', init);

  
})(window.spawnsong = {});

var a = 1;
