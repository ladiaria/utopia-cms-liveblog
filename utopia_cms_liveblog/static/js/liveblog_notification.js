function load_liveblog_notification(publication_slug){
  $("#liveblog-notifications").load("/liveblogs/notification/" + publication_slug + "/", function(response){
    if(response){
      $(".btn-close", this).click(function(){
        notification_close(this);
      });
    }
  });
}
