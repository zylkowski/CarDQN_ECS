import ecs
import data.components.segment as segment
import data.components.physics as physics
import data.components.texture_rendering as texture_rendering
import data.components.car_control as car_control
import data.components.DQNComponents as DQNComponents

class EntitySpawnerSystem(ecs.System):
    ENTITY_MANAGER = None

    def on_create(self):
        EntitySpawnerSystem.ENTITY_MANAGER = self.entity_manager

    def update(self, dt):
        pass
    
    @staticmethod
    def check_entity_manager_init():
        assert EntitySpawnerSystem.ENTITY_MANAGER is not None
    
    @staticmethod
    def spawn_segment(segment_type, start, end):
        EntitySpawnerSystem.check_entity_manager_init()
        
        segmentEntity = EntitySpawnerSystem.ENTITY_MANAGER.create_entity()
        EntitySpawnerSystem.ENTITY_MANAGER.add_component(segmentEntity, segment.SegmentComponent(start, end))
        EntitySpawnerSystem.ENTITY_MANAGER.add_component(segmentEntity, segment.SegmentTypeComponent(segment_type))

    @staticmethod
    def add_ray_to_entity(entity,length, angle):
        EntitySpawnerSystem.check_entity_manager_init()
        
        rayEntity = EntitySpawnerSystem.ENTITY_MANAGER.create_entity()
        EntitySpawnerSystem.ENTITY_MANAGER.add_component(rayEntity, segment.SegmentComponent((0, 0), (0, 0)))
        EntitySpawnerSystem.ENTITY_MANAGER.add_component(rayEntity, segment.SegmentRayComponent(entity,(0, 0), angle, length))
        EntitySpawnerSystem.ENTITY_MANAGER.add_component(rayEntity, segment.SegmentTypeComponent(segment.SegmentTypes.RAY))
        try:
            rayHolder: segment.SegmentRayHolder = EntitySpawnerSystem.ENTITY_MANAGER.component_for_entity(entity,
                                                                                          segment.SegmentRayHolder)
            rayHolder.add(rayEntity)
        except:
            EntitySpawnerSystem.ENTITY_MANAGER.add_component(entity,segment.SegmentRayHolder(rayEntity))
            
    @staticmethod
    def spawn_car_entity(pos,rot,car_texture_path):
        EntitySpawnerSystem.check_entity_manager_init()

        print(car_texture_path)
        carEntity = EntitySpawnerSystem.ENTITY_MANAGER.create_entity()
        EntitySpawnerSystem.ENTITY_MANAGER.add_component(carEntity, texture_rendering.TextureComponent(car_texture_path))
        EntitySpawnerSystem.ENTITY_MANAGER.add_component(carEntity, texture_rendering.TextureScale(0.2))

        EntitySpawnerSystem.ENTITY_MANAGER.add_component(carEntity, pos)
        EntitySpawnerSystem.ENTITY_MANAGER.add_component(carEntity, rot)
        EntitySpawnerSystem.ENTITY_MANAGER.add_component(carEntity, physics.Velocity((0, 0)))

        EntitySpawnerSystem.ENTITY_MANAGER.add_component(carEntity, car_control.CarControllerComponent(0.3, 0.01))
        EntitySpawnerSystem.ENTITY_MANAGER.add_component(carEntity, car_control.PlayerControlTag())

        EntitySpawnerSystem.ENTITY_MANAGER.add_component(carEntity, DQNComponents.DQNAgentData())
        EntitySpawnerSystem.ENTITY_MANAGER.add_component(carEntity, DQNComponents.DQNAgent(0.001,19,6))
        for angle in range(-40, 40, 5):
            EntitySpawnerSystem.add_ray_to_entity(carEntity, 400, angle)