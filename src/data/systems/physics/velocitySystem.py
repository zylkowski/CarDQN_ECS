import ecs
import numpy as np
import data.components.physics as physics

class VelocitySystem(ecs.System):
    def update(self, dt):
        self.entity_manager: ecs.EntityManager
        for entity, velocity in self.entity_manager.pairs_for_type(physics.Velocity):
            try:
                if dt < 100:
                    pos : physics.Position = self.entity_manager.component_for_entity(entity, physics.Position)
                    pos.pos = np.add(pos.pos,np.multiply(dt,velocity.vel))

            except:
                pass