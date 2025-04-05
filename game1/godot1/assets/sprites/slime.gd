extends Node2D

#const SPEED = 60
var SPEED = 60
# Called when the node enters the scene tree for the first time.
var direction = 1
@onready var ray_cast_right = $RayCastRight
@onready var ray_cast_left = $RayCastLeft
@onready var animated_sprite = $AnimatedSprite2D
@onready var gj_2 = $gj2
@onready var timer = $shouji/Timer
@onready var animation_player = $AnimationPlayer

var sc1 = 1
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if ray_cast_right.is_colliding():
		direction = -1
		animated_sprite.flip_h = true
	if ray_cast_left.is_colliding():
		direction = 1
		animated_sprite.flip_h = false 
	position.x += direction * SPEED * delta
	
	


func _on_shouji_area_entered(area:Area2D):
	SPEED = 0
	sc1 += 1
	animation_player.play("shouji1")
	print(sc1,"血量")
	#queue_free()
	print("受击")
	if sc1 == 5:
		queue_free()
	timer.start()
	
	
	
	


func _on_timer_timeout():
	SPEED = 60
	# Replace with function body.
