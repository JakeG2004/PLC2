# Assignment 1

## Product 1: Paper Coffee Sleeve
* Video link - https://www.youtube.com/watch?v=EoouKyWhoJY
* Process
  1. Corrugating
    * Separate machine which has multiple PLCS
    * PLC 1: Wet end
      * Big rolls of paper go across drums which have the corrugated pattern on them
      * PLC 2: "Starch kitchen" - Glue is made from a starch base and put onto paper
      * Corrugated part is pressed against flat paper ("liner") and glued
    * PLC 3: Dryer
      * Separate PLC
      * Belts are heated based on how fast they're running
      * Removes moisture from starch glue, leaving just adhesive
      * 100+ yards long
  2. Printing
    * Patterns printed on the "liner" prior to being glued to the fluted material
    * Unrolls paper, prints on it, then rolls it back up to be sent to the corrugator
    * Box @ 0:09 checks printing is correct
  3. Die Cutting
    * Material is cut to size, then is pushed down into the stack that the man works at
    * Likely uses flat-bed die cutter
    * Good product directed forward
    * Bad product collected for re-use / recycling
    * Makes many cuts all at the same time
    * 6-9K / hour
  4. Folder / Gluers
    * Flat sleeves are fed into the machine
    * Places glue on one side of sleeve
    * Folds non-glued side, then folds in the glued side
    * Typically different type of glue because better adhesion required
    * Uses UV cameras to verify that glue is placed in the right Places
  5. Compression
    * Sleeves are "shingled" and slowed down so that they can be in the shorter compression
    * Compression ensures glue is in the fibers of the sleeve
  6. Plastic Encapsulation
    * Food-grade materials require plastic wrapping
    * Material moved through in consistently sized chunks
  7. Case packing
    * Product placed into boxes and shipped off
* Safety PLC
  * Special type of PLC
  * Tracks redundancy channels
  * Shuts down system if one of them fails
* Props
  * Flat sheet of paper (if possible)
  * Sheet of corrugated
  * Cut out coffee sleeves
  * Folded sleeve
  * Glue to show process in real time?
* Potential sensors, actuators,or motors
  * Conveyor rollers / belts, heavy lifters. High voltage
    * Relays to switch high power devices
  * Small motors 
    * Relays to isolate spikes, electrical noise, etc...
  * Servo motors
  * Sensors
    * Inductive sensors - look for metal
    * Photo eyes - Sends out a signal and looks for a return signal with reflector
    * Diffused photo eyes - sends signal out and looks for return signal with no reflector
    * Thermistor / Thermometer / IR - temperature sensor
    * Encoders
    * Ultrasonic sensors
  * Actuators
    * Air valves
    * Jack screw
    * Heating element 
  * HMI
  * Buttons
* Block diagram
* What components are the most important datapoints that could be used for SCADA?

## Product 2: Tape Measures
* Video link - https://www.youtube.com/watch?v=-yqehvAQH1A
* Process
  1. Priming + Printing
    * Strips of steel are unrolled from big spools
    Brought through wheels which coat the steel in primer
    * Strips also painted at this time
    * Rewound into spools.
  2. Measurement markings
    * Strips are unrolled, and a stamp belt prints the measurement markings onto the steel Strips
    * Black ink used for smaller measurements, red ink used for larger element
  3. Coating + Heating
    * Thin plastic coating applied to protect paint
    * Tape heated to set the paint + The protective coating
  4. Shaping
    * Tape passed through several rollers which give the tape its U-shape
  5. Cutting
    * Tape is stopped after the appropriate length and are cut into individual tapes.
    * Hole punched for end-hook, riveted into placed
  6. Spring manufacturing
    * Same initial strip from before is tightly rolled to create a spring which retracts the measuring tape
  7. Automatic winding
    * Spring re-wound into the tape measure casing
  8. Humans do everything from there on out


