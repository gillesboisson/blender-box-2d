
PhysicsBodyType = (
    ("static", "Static", "Static body"), 
    ("dynamic", "Dynamic", "Dynamic body"), 
)

Physics2DBodyShapeType = (
    ("none", "None", "No shape"),
    ("box", "Box", "Box shape"),
    ("circle", "Circle", "Circle shape"),
    ("polygon", "Polygon", "Polygon shape"),
)


Physics3DBodyShapeType = (
    ("box", "Box", "Box shape"), 
    ("sphere", "Sphere", "Sphere shape"), 
    ("cylinder", "Cylinder", "Cylinder shape"), 
    ("mesh", "Mesh", "Mesh shape") 
)

ThreePhysicsMode = (
    ("disabled", "Disabled", "Disabled"), 
    ("2d", "Box 2D", "2D"),
    ("3d", "Ammo JS", "3D")
)

PlanDirection = (
    ('X', 'X', "X direction"), 
    ("Y", "Y", "Y direction"), 
    ('Z', 'Z', "Z direction"), 
)


ThreePhysicsMoveFreedoms = (
    ("XY", "XY", "XY"),
    ("X", "X", "X"),
    ("Y", "Y", "Y")
)
