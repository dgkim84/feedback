define([], function() {
  /**
   * repeat function. more functional!
   *
   * @param fn: function
   *   event callback
   * @param opts: object(times: int, interval: int)
   *   repeat options
   */
  function repeat(fn, opts) {
    opts = opts || {};
    opts.interval = opts.interval || 50;
    opts.times = opts.times === null ? 2 : opts.times;
    function repeat_inner() {
      opts.times = opts.times - 1;
      repeat(fn, opts);
    };
    var cont = fn(opts.times);
    if (cont !== false && opts.times > 1) {
      opts.timer = window.setTimeout(repeat_inner, opts.interval);
    }
    return {
      stop: function(fn) {
        try {
          if (opts.timer != null) {
            window.clearTimeout(opts.timer);
          }
        } catch (e) {}
        if (typeof(fn) == 'function') {
          fn();
        }
      }
    }
  };
  return {
    repeat: repeat
  };
});