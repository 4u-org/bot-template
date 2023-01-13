
var DemoApp = {
    initData: Telegram.WebApp.initData || '',
    initDataUnsafe: Telegram.WebApp.initDataUnsafe || {},
    MainButton: Telegram.WebApp.MainButton,
  
    init: function(options) {
      $('body').css('visibility', '');
      Telegram.WebApp.ready();
      Telegram.WebApp.MainButton.setParams({
        text: 'CLOSE WEBVIEW',
        is_visible: true
      }).onClick(DemoApp.close);
    },
    expand: function() {
      Telegram.WebApp.expand();
    },
    close: function() {
      Telegram.WebApp.close();
    },
    sendMessage: function(msg_id, with_webview) {
      if (!DemoApp.initDataUnsafe.query_id) {
        alert('WebViewQueryId not defined');
        return;
      }
      $('button').prop('disabled', true);
      $('#btn_status').text('Sending...').removeClass('ok err').show();
      DemoApp.apiRequest('sendMessage', {
        msg_id: msg_id || '',
        with_webview: !DemoApp.initDataUnsafe.receiver && with_webview ? 1 : 0
      }, function(result) {
        $('button').prop('disabled', false);
        if (result.response) {
          if (result.response.ok) {
            $('#btn_status').html('Message sent successfully!').addClass('ok').show();
          } else {
            $('#btn_status').text(result.response.description).addClass('err').show();
            alert(result.response.description);
          }
        } else if (result.error) {
          $('#btn_status').text(result.error).addClass('err').show();
          alert(result.error);
        } else {
          $('#btn_status').text('Unknown error').addClass('err').show();
          alert('Unknown error');
        }
      });
    },
    changeMenuButton: function(close) {
      $('button').prop('disabled', true);
      $('#btn_status').text('Changing button...').removeClass('ok err').show();
      DemoApp.apiRequest('changeMenuButton', {}, function(result) {
        $('button').prop('disabled', false);
        if (result.response) {
          if (result.response.ok) {
            $('#btn_status').html('Button changed!').addClass('ok').show();
            Telegram.WebApp.close();
          } else {
            $('#btn_status').text(result.response.description).addClass('err').show();
            alert(result.response.description);
          }
        } else if (result.error) {
          $('#btn_status').text(result.error).addClass('err').show();
          alert(result.error);
        } else {
          $('#btn_status').text('Unknown error').addClass('err').show();
          alert('Unknown error');
        }
      });
      if (close) {
        setTimeout(function() {
          Telegram.WebApp.close();
        }, 50);
      }
    },
    checkInitData: function() {
      if (DemoApp.initDataUnsafe.query_id &&
          DemoApp.initData &&
          $('#webview_data_status').hasClass('status_need')) {
        $('#webview_data_status').removeClass('status_need');
        DemoApp.apiRequest('checkInitData', {}, function(result) {
          if (result.ok) {
            $('#webview_data_status').html('Hash is correct (async)').addClass('ok');
          } else {
            $('#webview_data_status').html(result.error + ' (async)').addClass('err');
          }
        });
      }
    },
  
    sendText: function(spam) {
      var text = $('#text_field').val();
      if (!text.length) {
        return $('#text_field').focus();
      }
      if (byteLength(text) > 4096) {
        return alert('Text is too long');
      }
      var repeat = spam ? 10 : 1;
      for (var i = 0; i < repeat; i++) {
        Telegram.WebApp.sendData(text);
      }
    },
    sendTime: function(spam) {
      var repeat = spam ? 10 : 1;
      for (var i = 0; i < repeat; i++) {
        Telegram.WebApp.sendData(new Date().toString());
      }
    },
    requestLocation: function(el) {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
          $(el).next('span').html('(' + position.coords.latitude + ', ' + position.coords.longitude + ')').attr('class', 'ok');
        });
      } else {
        $(el).next('span').html('Geolocation is not supported in this browser.').attr('class', 'err');
      }
      return false;
    },
    requestVideo: function(el) {
      if (navigator.mediaDevices) {
        navigator.mediaDevices.getUserMedia({ audio: false, video: true }).then(function(stream) {
          $(el).next('span').html('(Access granted)').attr('class', 'ok');
        });
      } else {
        $(el).next('span').html('Media devices is not supported in this browser.').attr('class', 'err');
      }
      return false;
    },
    requestAudio: function(el) {
      if (navigator.mediaDevices) {
        navigator.mediaDevices.getUserMedia({ audio: true, video: false }).then(function(stream) {
          $(el).next('span').html('(Access granted)').attr('class', 'ok');
        });
      } else {
        $(el).next('span').html('Media devices is not supported in this browser.').attr('class', 'err');
      }
      return false;
    },
    toggleMainButton: function(el) {
      if (DemoApp.MainButton.isVisible) {
        DemoApp.MainButton.hide();
        el.innerHTML = 'Show Main Button';
      } else {
        DemoApp.MainButton.show();
        el.innerHTML = 'Hide Main Button';
      }
    },
    showAlert: function(message) {
      Telegram.WebApp.showAlert(message);
    },
    showConfirm: function(message) {
      Telegram.WebApp.showConfirm(message);
    },
    showPopup: function() {
      Telegram.WebApp.showPopup({
        title: 'Popup title',
        message: 'Popup message',
        buttons: [
          {id: 'delete', type: 'destructive', text: 'Delete all'},
          {id: 'faq', type: 'default', text: 'Open FAQ'},
          {type: 'cancel'},
        ]
      }, function(button_id) {
        if (button_id == 'delete') {
          DemoApp.showAlert("'Delete all' selected");
        } else if (button_id == 'faq') {
          Telegram.WebApp.openLink('https://telegram.org/faq');
        }
      });
    },
  
    apiRequest: function(method, data, onCallback) {
      var authData = DemoApp.initData || '';
      $.ajax('/demo/api', {
        type: 'POST',
        data: $.extend(data, {_auth: authData, method: method}),
        dataType: 'json',
        xhrFields: {
          withCredentials: true
        },
        success: function(result) {
          onCallback && onCallback(result);
        },
        error: function(xhr) {
          onCallback && onCallback({error: 'Server error'});
        }
      });
    }
  };
  
  var DemoAppMenu = {
    init: function() {
      DemoApp.init();
      $('body').addClass('gray');
      Telegram.WebApp.setHeaderColor('secondary_bg_color');
    }
  };
  
  var DemoAppInitData = {
    init: function() {
      DemoApp.init();
      // $('body').addClass('gray');
      // Telegram.WebApp.setHeaderColor('secondary_bg_color');
  
      Telegram.WebApp.onEvent('themeChanged', function() {
        $('#theme_data').html(JSON.stringify(Telegram.WebApp.themeParams, null, 2));
      });
      $('#webview_data').html(JSON.stringify(DemoApp.initDataUnsafe, null, 2));
      $('#theme_data').html(JSON.stringify(Telegram.WebApp.themeParams, null, 2));
      DemoApp.checkInitData();
  
  
    }
  };
  
  var DemoAppViewport = {
    init: function() {
      DemoApp.init();
      // $('body').addClass('gray');
      // Telegram.WebApp.setHeaderColor('secondary_bg_color');
      Telegram.WebApp.onEvent('viewportChanged', DemoAppViewport.setData);
      DemoAppViewport.setData();
    },
    setData: function() {
      $('.viewport-border').attr('text', window.innerWidth + ' x ' + round(Telegram.WebApp.viewportHeight, 2));
      $('.viewport-stable_border').attr('text', window.innerWidth + ' x ' + round(Telegram.WebApp.viewportStableHeight, 2) + ' | is_expanded: ' + (Telegram.WebApp.isExpanded ? 'true' : 'false'));
    }
  };
  
  function byteLength(str) {
    if (window.Blob) {
      try { return new Blob([str]).size; } catch (e) {}
    }
    var s = str.length;
    for (var i=str.length-1; i>=0; i--) {
      var code = str.charCodeAt(i);
      if (code > 0x7f && code <= 0x7ff) s++;
      else if (code > 0x7ff && code <= 0xffff) s+=2;
      if (code >= 0xDC00 && code <= 0xDFFF) i--;
    }
    return s;
  }
  
  function round(val, d) {
    var k = Math.pow(10, d || 0);
    return Math.round(val * k) / k;
  }