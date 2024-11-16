function load_liveblog_notification(base_path, publication_slug){
  let trigger_event = false;
  if (base_path && publication_slug) {
    $("#liveblog-notifications").load("/" + base_path + "/notification/" + publication_slug + "/", function(response){
      if (response) {
        $(".btn-close", this).click(function(){
          notification_close(this);
        });
      } else {
        trigger_event = true;
      }
    });
  } else {
    trigger_event = true;
  }
  if (trigger_event) {
    $(window).trigger("liveblog_notification_empty");
  }
}
