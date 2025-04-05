extends Control

@onready var v2 = $VBoxContainer
@onready var button_1 = $VBoxContainer/Button1
@onready var button_2 = $VBoxContainer/Button2
@onready var button_3 = $VBoxContainer/Button3
@onready var timer = $Timer


var server := UDPServer.new()
var peers = []
var status 
var last_action_time = 0.0 # 上次执行动作的时间
const ACTION_INTERVAL = 1.0 # 动作之间的最小间隔时间（秒）
var shen = 0
var sc1 = 1
func _ready() -> void:
	button_2.disabled = not has_savechang2()
	button_3.disabled = not has_savechang3()
	var first_button = v2.get_child(0)
	if first_button is Button:
		first_button.grab_focus()
	timer.start()
	## 开始监听端口7777
	#if server.listen(7777):
		#print("服务器正在监听端口7777...")
	#else:
		#print("无法监听指定端口")
	## 默认给予第一个按钮焦点
	#var first_button = v2.get_child(0)
	#if first_button is Button:
		#first_button.grab_focus()

func _physics_process(_delta):
	server.poll()
	while server.is_connection_available():
		var peer: PacketPeerUDP = server.take_connection()
		print("接受对等体：%s:%d" % [peer.get_packet_ip(), peer.get_packet_port()])
		peers.append(peer)

	# 处理来自所有已知对等体的数据包
	for peer in peers:
		while peer.get_available_packet_count() > 0:
			var packet = peer.get_packet()
			var message = String(packet.get_string_from_utf8())
			var parts = message.split(",")
			status = parts[0]
			print("接收到数据：%s" % [status])
			#if status == "c":
			
			
			if Time.get_ticks_msec() - last_action_time >= ACTION_INTERVAL * 1000:
				if status == "b":
					move_focus_to_next_button()
				elif status == "a":
					move_focus_to_previous_button()
				elif status == "c":
					click_focused_button()
				last_action_time = Time.get_ticks_msec()
			
			# 进行回复，这样对方就知道我们收到了消息。
			peer.put_packet(packet)
	if status == "f":
	#if Input.is_action_pressed("ui_cancel"):
		get_tree().change_scene_to_file("res://scenes/title_screen.tscn")

func move_focus_to_next_button():
	var current_focus = null
	for button in v2.get_children():
		if button.has_focus():
			current_focus = button
			break
	
	if current_focus:
		var children = v2.get_children()
		var index = children.find(current_focus)
		if index != -1 && index < children.size() - 1:
			var next_button = children[index + 1]
			if next_button is Button:
				next_button.grab_focus()
		elif index == children.size() - 1:
			# 如果当前按钮是最后一个，则返回到第一个按钮
			var first_button = children[0]
			if first_button is Button:
				first_button.grab_focus()

func move_focus_to_previous_button():
	var current_focus = null
	for button in v2.get_children():
		if button.has_focus():
			current_focus = button
			break
	
	if current_focus:
		var children = v2.get_children()
		var index = children.find(current_focus)
		if index > 0:
			var prev_button = children[index - 1]
			if prev_button is Button:
				prev_button.grab_focus()
		elif index == 0:
			# 如果当前按钮是第一个，则循环到最后一个按钮
			var last_button = children[children.size() - 1]
			if last_button is Button:
				last_button.grab_focus()

func click_focused_button():
	var current_focus = null
	for button in v2.get_children():
		if button.has_focus():
			current_focus = button
			break
	
	if current_focus and current_focus is Button:
		# 根据按钮身份调用相应的点击处理函数
		if current_focus == button_1:
			_on_button_1_pressed()
		elif current_focus == button_2:
			_on_button_2_pressed()
		elif current_focus == button_3:
			_on_button_3_pressed()


func _on_new_game_pressed():
	# 尝试删除 savegame.tres 文件
	var savegame_deleted = DirAccess.remove_absolute("user://savegame.tres")
	# 尝试删除 savescore.tres 文件
	var savescore_deleted = DirAccess.remove_absolute("user://savescore.tres")
	DirAccess.remove_absolute("user://savexie.tres")
	DirAccess.remove_absolute("user://saveslime.tres")
	#var _loadshenchu_deleted = DirAccess.remove_absolute("user://saveshenchu.tres")
	# 输出删除状态（可选）
	if savegame_deleted:
		print("savegame.tres 已删除")
	else:
		print("savegame.tres 不存在或删除失败")
	
	if savescore_deleted:
		print("savescore.tres 已删除")
	else:
		print("savescore.tres 不存在或删除失败")
	
	# 无论文件是否删除成功，都尝试切换场景
	get_tree().change_scene_to_file("res://game.tscn")

func _on_load_game_pressed():
	if  has_saveshenchu():
		_loadshenchu()
		if shen == 3:
			get_tree().change_scene_to_file("res://scenes/game_3.tscn")
			print("加载场景3！！！")
		elif  shen == 2:
			get_tree().change_scene_to_file("res://scenes/game_2.tscn")
		else :
			get_tree().change_scene_to_file("res://game.tscn")
	else :
		get_tree().change_scene_to_file("res://game.tscn")

func _on_exit_game_pressed():
	get_tree().quit()

func has_save() -> bool:
	var save_path = "user://savegame.tres"
	return FileAccess.file_exists(save_path)
	
func has_saveshenchu() -> bool:
	var save_path = "user://saveshenchu.tres"
	return FileAccess.file_exists(save_path)
func _loadshenchu():
	var data = FileAccess.open("user://saveshenchu.tres",FileAccess.READ) 
	shen = data.get_var()


func _on_guanka_pressed():
	get_tree().change_scene_to_file("res://scenes/gunaka.tscn")


func _on_button_1_pressed():
	DirAccess.remove_absolute("user://savegame.tres")
	DirAccess.remove_absolute("user://savescore.tres")
	DirAccess.remove_absolute("user://savexie.tres")
	DirAccess.remove_absolute("user://saveslime.tres")
	DirAccess.remove_absolute("user://guan2.tres")
	DirAccess.remove_absolute("user://guan3.tres")
	get_tree().change_scene_to_file("res://game.tscn")


func _on_button_2_pressed():
	DirAccess.remove_absolute("user://savegame.tres")
	DirAccess.remove_absolute("user://savescore.tres")
	DirAccess.remove_absolute("user://savexie.tres")
	DirAccess.remove_absolute("user://saveslime.tres")
	DirAccess.remove_absolute("user://savesc1_1_2.tres")
	DirAccess.remove_absolute("user://chuan.tres")
	DirAccess.remove_absolute("user://guan2.tres")
	DirAccess.remove_absolute("user://guan3.tres")
	var file3 = FileAccess.open("user://guan2.tres",FileAccess.WRITE)
	file3.store_var(sc1)
	file3.close()
	get_tree().change_scene_to_file("res://scenes/game_2.tscn")


func _on_button_3_pressed():
	DirAccess.remove_absolute("user://savegame.tres")
	DirAccess.remove_absolute("user://savescore.tres")
	DirAccess.remove_absolute("user://savexie.tres")
	DirAccess.remove_absolute("user://saveslime.tres")
	DirAccess.remove_absolute("user://savesc1_1_2.tres")
	DirAccess.remove_absolute("user://chuan.tres")
	DirAccess.remove_absolute("user://guan2.tres")
	DirAccess.remove_absolute("user://guan3.tres")
	var file3 = FileAccess.open("user://guan3.tres",FileAccess.WRITE)
	file3.store_var(sc1)
	file3.close()
	get_tree().change_scene_to_file("res://scenes/game_3.tscn")


func _on_timer_timeout():
	# 开始监听端口7777
	if server.listen(7777):
		print("服务器正在监听端口7777...")
	else:
		print("无法监听指定端口")
	# 默认给予第一个按钮焦点
	#var first_button = v2.get_child(0)
	#if first_button is Button:
		#first_button.grab_focus()
		
func has_savechang2() -> bool:
	var save_path = "user://savechang2.tres"
	return FileAccess.file_exists(save_path)

func has_savechang3() -> bool:
	var save_path = "user://savechang3.tres"
	return FileAccess.file_exists(save_path)
