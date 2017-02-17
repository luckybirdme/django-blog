$(function () {
	$("textarea[name='markdown']").bind('input propertychange change', function() {
		var self = $(this);
		var markdown = self.val();
		var preview = marked(markdown);
		$("#preview").html(preview);
		$("input[name='content']").val(preview);
	});

	$("textarea[name='markdown']").trigger('change');

	if (typeof(Worker) !== "undefined") {
		$("textarea[name='markdown']").get(0).addEventListener("drop",
			function(e) {
				var self = $(this);
			    e.preventDefault(); //取消默认浏览器拖拽效果
			    var fileList = e.dataTransfer.files; //获取文件对象
			    //检测是否是拖拽文件到页面的操作
			    if (fileList.length == 0) {
			        return false;
			    }
			    //检测文件是不是图片
			    if (fileList[0].type.indexOf('image') === -1) {
			        alert("File is not image");
			        return false;
			    }
			    //拖拉图片到浏览器，可以实现预览功能
			    var img = window.webkitURL.createObjectURL(fileList[0]);
			    var filename = fileList[0].name; //图片名称
			    var filesize = Math.floor((fileList[0].size) / 1024);
			    if (filesize > 500) { // 500k
			        alert("File is large than 500KB");
			        return false;
			    }
			    //alert(filesize);

			    //上传
			    xhr = new XMLHttpRequest();

				// 设置超时，单位秒；
				xhr.timeout = 10000; 
				// 超时处理函数
				xhr.ontimeout = function (e) {
				  // XMLHttpRequest timed out. Do something here.
				  alert('Timeout');
				};

				// 请求返回处理
				xhr.onreadystatechange = function() {
				        // 读取对象状态
					if (xhr.readyState == XMLHttpRequest.DONE) {
				                // 读取返回状态和结果，200表示http请求成功
						if (xhr.status == 200) {
				                        // 获取返回数据
							var response =  xhr.responseText;
							var oldval = self.val();
						    var markdown_image = "![image]("+response+")";
						    var newval = oldval + markdown_image;
						    self.val(newval);
						    self.change();

						} else {
				            // 异常处理
							alert('something wrong');
						}
					}

				} 

				var url = $("#upload").attr('url');
			    xhr.open("post", url, true);
			    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

			   	
			    var csrf = $("input[name='csrfmiddlewaretoken']").val();
			    var fd = new FormData();
			    fd.append('upload', fileList[0]);
			    fd.append('csrfmiddlewaretoken', csrf);

			    xhr.send(fd);


			   

			},false);

	} else {
	    console.log("Unable to upload image");
	}



});