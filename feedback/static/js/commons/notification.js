/**
 * very simple notification library
 *
 * @author Daegeun Kim
 */
define([], function() {
  queue = [];

  function positioning() {
    if (queue.length == 0) {
      return 20
    } else {
      var padding = 10;
      var last = queue[queue.length - 1];
      var top = last.position().top + last.outerHeight() + padding;
      var height = $(document).outerHeight();
      if (top > height - 50) {
        return 20;
      }
      return top;
    }
  };

  function init(opts) {
    var top = $('<div class="alert alert-'+opts.type+'"></div>');
    top.css('position', 'absolute');
    top.css('top', positioning() + 'px');
    top.css('right', '50px');
    top.css('alpha', '50%');
    top.css('width', '400px');
    var inner = $('<div>'+(opts.title ? '<strong>'+opts.title+'</strong> ' : '')+opts.message+'</div>').appendTo(top);
    top.on('click', function() {
      top.remove();
    });
    top.hide().fadeIn(100).delay(5000).fadeOut(5000, function() {
      top.remove();
    });
    return top;
  };

  function pop(type) {
    return function(opts) {
      if (typeof(opts) == 'string') {
        opts = {message: opts};
      }
      opts = opts || {};
      opts.type = type;
      if (opts.message) {
        var element = init(opts);
        queue.push(element);
        $(element).appendTo($(document.body));
      }
    }
  };

  return {
    success: pop('success'),
    info: pop('info'),
    error: pop('error')
  };
});