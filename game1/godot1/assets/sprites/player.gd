extends CharacterBody2D
class_name Player


@onready var label_4 = $ZhuangTai/TextureRect/Label4

@onready var game_manager = %GameManager

@onready var animation_player = $gj2/AnimationPlayer
@onready var gj_2 = $gj2
@onready var timer = $Timer

@onready var collision_shape_2d_2 = $Area2D/CollisionShape2D2
@onready var animation_player3 = $aida1/AnimationPlayer

@onready var animation_player2 = $AnimationPlayer
@onready var texture_rect_2 = $ZhuangTai/TextureRect2
@onready var texture_rect_3 = $ZhuangTai/TextureRect3
@onready var texture_rect_4 = $ZhuangTai/TextureRect4

@onready var game = $".."

@onready var timer_2 = $Timer2
@onready var huixie = $huixie

@onready var huixiejiange = $huixiejiange
@onready var meiqian = $meiqian
@onready var meiqian_1 = $meiqian1


@onready var timer_3 = $Timer3

@onready var xl_1 = $CanvasLayer/xl1
@onready var xl_2 = $CanvasLayer/xl2
@onready var xl_3 = $CanvasLayer/xl3

@onready var label_6 = $CanvasLayer/TextureRect/Label6
@onready var label_7 = $CanvasLayer/TextureRect/Label7

@onready var xl_3_1 = $CanvasLayer/xl3_1
@onready var xl_3_2 = $CanvasLayer/xl3_2
@onready var xl_3_3 = $CanvasLayer/xl3_3

@onready var save_slime = $"../Slime/Node/SaveSlime"
@onready var saveslime_2 = $"../Slime02/Node/saveslime2"
@onready var saveslime_3 = $"../SLIME/Node/saveslime3"


#@onready var label_4 = $CanvasLayer/TextureRect/Label4


const SPEED = 130.0
const JUMP_VELOCITY = -280.0
var server := UDPServer.new()
var server2 := UDPServer.new()
var server3 := UDPServer.new()
var peers = []
var peers2 = []
var peers3 = []
var str1
var status 
var cx1 
var jump_status 
var gongji
var sc1 = 0
var xl1 = 0
var xl2 = 0
var xl3 = 0
var sc1_2 = 0
var xl2_1 = 0
var xl2_2 = 0
var xl2_3 = 0
var xl3_1 = 0
var xl3_2 = 0
var xl3_3 = 0

func _ready():
	meiqian.hide()
	huixie.hide()
	animation_player3.play("kaichang1")
	animation_player.play("goji2")
	gj_2.hide()
	gj_2.monitorable = false
	timer_3.start()
	 # 禁用碰撞检测
	if has_save():
		_load()
	# 开始监听端口7777
	if has_shou():
		if server.listen(7777):
			print("服务器正在监听端口7777...")
		else:
			print("无法监听指定端口")
		if server2.listen(7778):
			print("7778")
		else :
			print("无法监听7778")
		if server3.listen(7779):
			print("7778")
		else :
			print("无法监听7779")
	


# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")
@onready var animated_sprite = $AnimatedSprite2D

func _save() -> void:
	var file = FileAccess.open("user://savegame.tres",FileAccess.WRITE)
	file.store_var(global_position)
	file.store_var(animated_sprite.flip_h) # 保存朝向
	file.store_var(sc1)
	#file.store_var(label_4.text)
	file.close()
	var file2 = FileAccess.open("user://savexie.tres",FileAccess.WRITE)
	file2.store_var(sc1)
	file2.store_var(xl1)
	file2.store_var(xl2)
	file2.store_var(xl3)
	file2.close()
	print("saved!")
func _save2():
	var file = FileAccess.open("user://savegame.tres",FileAccess.WRITE)
	file.store_var(global_position)
	file.store_var(animated_sprite.flip_h) # 保存朝向
	file.store_var(sc1)
	#file.store_var(label_4.text)
	file.close()
	var file2 = FileAccess.open("user://savexie.tres",FileAccess.WRITE)
	file2.store_var(sc1)
	file2.store_var(xl2_1)
	file2.store_var(xl2_2)
	file2.store_var(xl2_3)
	file2.close()
	print("saved--2!")
func _save3():
	var file = FileAccess.open("user://savegame.tres",FileAccess.WRITE)
	file.store_var(global_position)
	file.store_var(animated_sprite.flip_h) # 保存朝向
	file.store_var(sc1)
	#file.store_var(label_4.text)
	file.close()
	var file2 = FileAccess.open("user://savexie.tres",FileAccess.WRITE)
	file2.store_var(sc1)
	file2.store_var(xl3_1)
	file2.store_var(xl3_2)
	file2.store_var(xl3_3)
	file2.close()
	print("saved--3!")


func has_chang1() -> bool:
	var save_path = "user://savechang1.tres"
	return FileAccess.file_exists(save_path)
	


func has_save() -> bool:
	var save_path = "user://savegame.tres"
	return FileAccess.file_exists(save_path)

func _on_escape_pressed():
	get_tree().change_scene_to_file("res://scenes/title_screen.tscn")

func _load() -> void:
	var data = FileAccess.open("user://savegame.tres",FileAccess.READ) 
	global_position = data.get_var()
	animated_sprite.flip_h = data.get_var() # 加载朝向
	sc1 = data.get_var()
	#var data2 = FileAccess.open("user://savexie.tres",FileAccess.READ) 
	#sc1 = data2.get_var()
	#xl1 = data2.get_var()
	#xl2 = data2.get_var()
	#xl3 = data2.get_var()
	#if xl1 == 1:
		#texture_rect_2.hide()
	#if xl2 == 1:
		#texture_rect_3.hide()
	#if xl3 == 1:
		#texture_rect_4.hide()
	#label_4.text = data.get_var()
	print(position)
	move_and_slide()
	#animated_sprite.flip_h = data.is_facing_Left
	#get_child(0).flip_h = data.is_facing_Left
	print("loaded!")
	

func _physics_process(delta):
	server.poll()
	while server.is_connection_available():
		var peer: PacketPeerUDP = server.take_connection()
		print("接受对等体：%s:%d" % [peer.get_packet_ip(), peer.get_packet_port()])
		peers.append(peer)
	server2.poll()
	while server2.is_connection_available():
		var peer2: PacketPeerUDP = server2.take_connection()
		print("接受对等体：%s:%d" % [peer2.get_packet_ip(), peer2.get_packet_port()])
		peers2.append(peer2)
	server3.poll()
	while server3.is_connection_available():
		var peer3: PacketPeerUDP = server3.take_connection()
		print("接受对等体：%s:%d" % [peer3.get_packet_ip(), peer3.get_packet_port()])
		peers3.append(peer3)
	
	# 处理来自所有已知对等体的数据包
	for peer in peers:
		while peer.get_available_packet_count() > 0:
			var packet = peer.get_packet()
			var message = String(packet.get_string_from_utf8())
			var parts = message.split(",")
			status = parts[0]
			# 进行回复，这样对方就知道我们收到了消息。
			peer.put_packet(packet)
	for peer2 in peers2:
		while peer2.get_available_packet_count() > 0:
			var packet2 = peer2.get_packet()
			var message2 = String(packet2.get_string_from_utf8())
			var parts2 = message2.split(",")
			gongji = parts2[0]
			jump_status = parts2[1].to_int()
			print("接收到数据：%s, cx : %d, 跳跃状态：%d" % [status,cx1,jump_status])
			# 进行回复，这样对方就知道我们收到了消息。
			peer2.put_packet(packet2)
			
	for peer3 in peers3:
		while peer3.get_available_packet_count() > 0:
			var packet3 = peer3.get_packet()
			var message3 = String(packet3.get_string_from_utf8())
			var parts3 = message3.split(",")
			cx1 = parts3[0].to_int()
			# 进行回复，这样对方就知道我们收到了消息。
			peer3.put_packet(packet3)
	# Add the gravity.
	if not is_on_floor():
		velocity.y += gravity * delta

	# Handle jump.
	#if Input.is_action_just_pressed("jump") and is_on_floor():
	if has_shou():
		if jump_status == 2 and is_on_floor():
			velocity.y = JUMP_VELOCITY
	elif  Input.is_action_just_pressed("jump") and is_on_floor():		
			velocity.y = JUMP_VELOCITY
		#var sc1_2 = game_2.changjing
		#print(sc1_2)

	# Get the input direction and handle the movement/deceleration.
	# As good practice, you should replace UI actions with custom gameplay actions.
	#获取驶入方向direction:-1, 0, 1
	var direction = Input.get_axis("move_left", "move_right")
	if has_shou():
		if status == "f":
		#if Input.is_action_pressed("ui_cancel"):
			if sc1_2 == 1:
				label_4._save()
				_save()
				_saveshenchu()
				_on_escape_pressed()
				save_slime._save()
			elif sc1_2 == 2:
				label_6._save()
				_save2()
				_saveshenchu()
				saveslime_2._save()
				_on_escape_pressed()
				DirAccess.remove_absolute("user://chuan.tres")
			elif sc1_2 == 3:
				label_7._save()
				_save3()
				_saveshenchu()
				saveslime_3._save()
				_on_escape_pressed()
				DirAccess.remove_absolute("user://chuan.tres")
	elif  Input.is_action_pressed("ui_cancel"):
			if sc1_2 == 1:
				label_4._save()
				_save()
				_saveshenchu()
				_on_escape_pressed()
				save_slime._save()
			elif sc1_2 == 2:
				label_6._save()
				_save2()
				_saveshenchu()
				saveslime_2._save()
				_on_escape_pressed()
				DirAccess.remove_absolute("user://chuan.tres")
			elif sc1_2 == 3:
				label_7._save()
				_save3()
				_saveshenchu()
				saveslime_3._save()
				_on_escape_pressed()
				DirAccess.remove_absolute("user://chuan.tres")
		
	#var direction = 0
	if cx1 == 3:
		direction = 1
	elif cx1 == 1:
		direction = -1
	#翻转精灵
	if direction > 0 :
		animated_sprite.flip_h = false
	elif direction < 0 :
		animated_sprite.flip_h = true
	if has_shou():
		if status == "e":	
		#if Input.is_action_just_pressed("huixie"):
			if sc1_2 == 1:
				if sc1 == 0:
					pass
				else :
					var qian = label_4._huixie1()
					if qian == 1:
						if sc1 == 1:
							xl3 = 0
							texture_rect_4.show()
							sc1 -= 1
							huixie.show()
							huixiejiange.start()
						elif sc1 == 2:
							xl2 = 0
							texture_rect_3.show()
							sc1 -= 1
							huixie.show()
							huixiejiange.start()
					elif qian == 2:
						meiqian.show()
						meiqian_1.start()
			elif  sc1_2 == 2:
				if sc1 == 0:
					pass
				else :
					var qian = label_6._huixie1()
					if qian == 1:
						if sc1 == 1:
							xl2_3 = 0
							xl_3.show()
							sc1 -= 1
							huixie.show()
							huixiejiange.start()
						elif sc1 == 2:
							xl2_2 = 0
							xl_2.show()
							sc1 -= 1
							huixie.show()
							huixiejiange.start()
					elif qian == 2:
						meiqian.show()
						meiqian_1.start()	
			elif  sc1_2 == 3:
				if sc1 == 0:
					pass
				else :
					var qian = label_7._huixie1()
					if qian == 1:
						if sc1 == 1:
							xl3_3 = 0
							xl_3_3.show()
							sc1 -= 1
							huixie.show()
							huixiejiange.start()
						elif sc1 == 2:
							xl3_2 = 0
							xl_3_2.show()
							sc1 -= 1
							huixie.show()
							huixiejiange.start()
					elif qian == 2:
						meiqian.show()
						meiqian_1.start()	
	elif  Input.is_action_just_pressed("huixie"):
			if sc1_2 == 1:
				if sc1 == 0:
					pass
				else :
					var qian = label_4._huixie1()
					if qian == 1:
						if sc1 == 1:
							xl3 = 0
							texture_rect_4.show()
							sc1 -= 1
							huixie.show()
							huixiejiange.start()
						elif sc1 == 2:
							xl2 = 0
							texture_rect_3.show()
							sc1 -= 1
							huixie.show()
							huixiejiange.start()
					elif qian == 2:
						meiqian.show()
						meiqian_1.start()
			elif  sc1_2 == 2:
				if sc1 == 0:
					pass
				else :
					var qian = label_6._huixie1()
					if qian == 1:
						if sc1 == 1:
							xl2_3 = 0
							xl_3.show()
							sc1 -= 1
							huixie.show()
							huixiejiange.start()
						elif sc1 == 2:
							xl2_2 = 0
							xl_2.show()
							sc1 -= 1
							huixie.show()
							huixiejiange.start()
					elif qian == 2:
						meiqian.show()
						meiqian_1.start()	
			elif  sc1_2 == 3:
				if sc1 == 0:
					pass
				else :
					var qian = label_7._huixie1()
					if qian == 1:
						if sc1 == 1:
							xl3_3 = 0
							xl_3_3.show()
							sc1 -= 1
							huixie.show()
							huixiejiange.start()
						elif sc1 == 2:
							xl3_2 = 0
							xl_3_2.show()
							sc1 -= 1
							huixie.show()
							huixiejiange.start()
					elif qian == 2:
						meiqian.show()
						meiqian_1.start()	
		  #sc1 == 1:
			#xl3 = 0
			#texture_rect_4.show()
			#sc1 -= 1
			#huixie.show()
			#huixiejiange.start()
			
	if has_shou():	
		if gongji == "d":
		#if Input.is_action_pressed("goji1") :
			gj_2.monitorable = true
			if animated_sprite.flip_h == false:
				gj_2.show()
				#print("攻击")
				animation_player.play("goji2")
				timer.start()
				
			elif animated_sprite.flip_h == true :
				gj_2.show()
				#print("攻击")
				animation_player.play("goji3")
				timer.start()
	elif Input.is_action_pressed("goji1") :
		gj_2.monitorable = true
		if animated_sprite.flip_h == false:
			gj_2.show()
			#print("攻击")
			animation_player.play("goji2")
			timer.start()
					
		elif animated_sprite.flip_h == true :
			gj_2.show()
			#print("攻击")
			animation_player.play("goji3")
			timer.start()
		
	if is_on_floor():
		if direction == 0:
			animated_sprite.play("idle")
		else :
			animated_sprite.play("run")
	else :
		animated_sprite.play("jump")
			
		
	if direction:
		velocity.x = direction * SPEED
	else:
		velocity.x = move_toward(velocity.x, 0, SPEED)
	

	move_and_slide()




func _on_timer_timeout():
	gj_2.monitorable = false
	gj_2.hide() # Replace with function body.
	
func _chupeng1():
	if sc1_2 == 1:
		if sc1 == 0:
			sc1 += 1
			xl3 = 1
			animation_player3.play("aida1")
			texture_rect_4.hide()
		elif sc1 == 1:
			sc1 += 1
			xl2 = 1
			animation_player3.play("aida1")
			texture_rect_3.hide()
		elif sc1 == 2:
			xl1 = 1
			animation_player3.play("aida1")
			texture_rect_2.hide()
			print("you died!") # Replace with function body.
			DirAccess.remove_absolute("user://savegame.tres")
			DirAccess.remove_absolute("user://savescore.tres")
			DirAccess.remove_absolute("user://savexie.tres")
			DirAccess.remove_absolute("user://saveslime.tres")
			print("删除成功！")	
			Engine.time_scale = 0.5
			get_node("CollisionShape2D").queue_free()
			timer_2.start()
			
	elif sc1_2 == 2:
		if sc1 == 0:
			sc1 += 1
			xl2_3 = 1
			animation_player3.play("aida1")
			xl_3.hide()
		elif sc1 == 1:
			sc1 += 1
			xl2_2 = 1
			animation_player3.play("aida1")
			xl_2.hide()
		elif sc1 == 2:
			xl2_1 = 1
			animation_player3.play("aida1")
			xl_1.hide()
			print("you died!") # Replace with function body.
			DirAccess.remove_absolute("user://savegame.tres")
			DirAccess.remove_absolute("user://savescore.tres")
			DirAccess.remove_absolute("user://savesc1_1_2.tres")
			DirAccess.remove_absolute("user://savexie.tres")
			DirAccess.remove_absolute("user://saveslime.tres")
			print("删除成功！")	
			Engine.time_scale = 0.5
			get_node("CollisionShape2D").queue_free()
			timer_2.start()
	elif sc1_2 == 3:
		if sc1 == 0:
			sc1 += 1
			xl3_3 = 1
			animation_player3.play("aida1")
			xl_3_3.hide()
		elif sc1 == 1:
			sc1 += 1
			xl3_2 = 1
			animation_player3.play("aida1")
			xl_3_2.hide()
		elif sc1 == 2:
			xl3_1 = 1
			animation_player3.play("aida1")
			xl_3_1.hide()
			print("you died!") # Replace with function body.
			DirAccess.remove_absolute("user://savegame.tres")
			DirAccess.remove_absolute("user://savescore.tres")
			DirAccess.remove_absolute("user://savesc1_1_2.tres")
			DirAccess.remove_absolute("user://savexie.tres")
			DirAccess.remove_absolute("user://saveslime.tres")
			print("删除成功！")	
			Engine.time_scale = 0.5
			get_node("CollisionShape2D").queue_free()
			timer_2.start()


func _on_timer_2_timeout():
	Engine.time_scale = 1.0
	if has_saveguan2():
		get_tree().change_scene_to_file("res://scenes/game_2.tscn")
	elif has_saveguan3():
		get_tree().change_scene_to_file("res://scenes/game_3.tscn")
	else :
		get_tree().change_scene_to_file("res://game.tscn")
	#get_tree().change_scene_to_file("res://game.tscn")
	
	 # Replace with function body.


func _on_huixiejiange_timeout():
	huixie.hide()
	
	# Replace with function body.


func _on_meiqian_1_timeout():
	meiqian.hide()
	 # Replace with function body.

func has_save_xie1() -> bool:
	var save_path = "user://savexie.tres"
	return FileAccess.file_exists(save_path)

func _on_timer_3_timeout():
	sc1_2 = game.changjing
	print(sc1_2)
	if sc1_2 == 1:
		if has_save_xie1():
			var data2 = FileAccess.open("user://savexie.tres",FileAccess.READ) 
			sc1 = data2.get_var()
			xl1 = data2.get_var()
			xl2 = data2.get_var()
			xl3 = data2.get_var()
	if sc1_2 == 2:
		if has_savesc1_1_2():	
			var data = FileAccess.open("user://savexie.tres",FileAccess.READ) 
			sc1 = data.get_var()
			xl2_1 = data.get_var()
			xl2_2 = data.get_var()
			xl2_3 = data.get_var()
	if sc1_2 == 3:
		if has_savesc1_1_2():
			var data = FileAccess.open("user://savexie.tres",FileAccess.READ) 
			sc1 = data.get_var()
			xl3_1 = data.get_var()
			xl3_2 = data.get_var()
			xl3_3 = data.get_var()
		
		
	 # Replace with function body.
	
func _savesc1_1_2():
	var file = FileAccess.open("user://savesc1_1_2.tres",FileAccess.WRITE)
	file.store_var(sc1)
	file.close()
	
func has_savesc1_1_2() -> bool:
	var save_path = "user://savesc1_1_2.tres"
	return FileAccess.file_exists(save_path)

func _saveshenchu():
	var file = FileAccess.open("user://saveshenchu.tres",FileAccess.WRITE)
	file.store_var(sc1_2)
	print("sc1_2的值是：",sc1_2)
	file.close()

func has_saveguan2() -> bool:
	var save_path = "user://guan2.tres"
	return FileAccess.file_exists(save_path)

func has_saveguan3() -> bool:
	var save_path = "user://guan3.tres"
	return FileAccess.file_exists(save_path)

func has_shou() -> bool:
	var save_path = "user://shou.tres"
	return FileAccess.file_exists(save_path)
