import ecs
import data.components.segment as segment
import data.components.physics as physics
import data.components.texture_rendering as texture_rendering
import data.components.car_control as car_control
import data.components.DQNComponents as DQNComponents

class EntitySpawnerSystem(ecs.System):
    entity_manager = None

    def on_create(self):
        EntitySpawnerSystem.entity_manager = self.entity_manager


    def update(self, dt):
        pass
    
    @staticmethod
    def check_entity_manager_init():
        assert EntitySpawnerSystem.entity_manager is not None
    
    @staticmethod
    def spawn_segment(segment_type, start, end):
        EntitySpawnerSystem.check_entity_manager_init()
        
        segmentEntity = EntitySpawnerSystem.entity_manager.create_entity()
        EntitySpawnerSystem.entity_manager.add_component(segmentEntity, segment.SegmentComponent(start, end))
        EntitySpawnerSystem.entity_manager.add_component(segmentEntity, segment.SegmentTypeComponent(segment_type))

    @staticmethod
    def add_ray_to_entity(entity,length, angle):
        EntitySpawnerSystem.check_entity_manager_init()
        
        rayEntity = EntitySpawnerSystem.entity_manager.create_entity()
        EntitySpawnerSystem.entity_manager.add_component(rayEntity, segment.SegmentComponent((0, 0), (0, 0)))
        EntitySpawnerSystem.entity_manager.add_component(rayEntity, segment.SegmentRayComponent(entity,(0, 0), angle, length))
        EntitySpawnerSystem.entity_manager.add_component(rayEntity, segment.SegmentTypeComponent(segment.SegmentTypes.RAY))
        try:
            rayHolder: segment.SegmentRayHolder = EntitySpawnerSystem.entity_manager.component_for_entity(entity,
                                                                                          segment.SegmentRayHolder)
            rayHolder.add(rayEntity)
        except:
            EntitySpawnerSystem.entity_manager.add_component(entity,segment.SegmentRayHolder(rayEntity))
            
    @staticmethod
    def spawn_car_entity(pos,rot,car_texture_path):
        EntitySpawnerSystem.check_entity_manager_init()

        carEntity = EntitySpawnerSystem.entity_manager.create_entity()
        EntitySpawnerSystem.entity_manager.add_component(carEntity, texture_rendering.TextureComponent(car_texture_path))
        EntitySpawnerSystem.entity_manager.add_component(carEntity, texture_rendering.TextureScale(0.2))

        EntitySpawnerSystem.entity_manager.add_component(carEntity, pos)
        EntitySpawnerSystem.entity_manager.add_component(carEntity, rot)
        EntitySpawnerSystem.entity_manager.add_component(carEntity, physics.Velocity((0, 0)))

        EntitySpawnerSystem.entity_manager.add_component(carEntity, car_control.CarControllerComponent(0.3, 0.01))
        EntitySpawnerSystem.entity_manager.add_component(carEntity, car_control.PlayerControlTag())

        EntitySpawnerSystem.entity_manager.add_component(carEntity, DQNComponents.DQNAgentData())
        EntitySpawnerSystem.entity_manager.add_component(carEntity, DQNComponents.DQNAgent(0.001,19,6))
        for angle in range(-40, 40, 5):
            EntitySpawnerSystem.add_ray_to_entity(carEntity, 400, angle)
