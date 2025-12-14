#!/usr/bin/env python
"""
Скрипт для создания базы знаний с заменой терминов.
Создает 30+ документов на основе вселенной, заменяя термины на вымышленные.
"""

import json
import os
from pathlib import Path

# Загружаем словарь замен
with open("knowledge_base/terms_map.json", "r", encoding="utf-8") as f:
    terms_map = json.load(f)


def replace_terms(text: str, terms_dict: dict) -> str:
    """Заменяет все термины в тексте согласно словарю"""
    result = text
    # Сортируем по длине (от длинных к коротким) чтобы избежать частичных замен
    for original, replacement in sorted(terms_dict.items(), key=lambda x: len(x[0]), reverse=True):
        result = result.replace(original, replacement)
    return result


# База документов о вселенной Star Wars (которые будут преобразованы)
documents = {
    "01_synth_flux_overview.md": """# Synth Flux Overview

Synth Flux is an energy field that permeates the entire QuantumVerse universe. It binds together all living things and gives SynthKeepers their extraordinary abilities.

## Properties

The Synth Flux has two aspects:
- **Synth Harmony**: Used by SynthKeepers for protection and knowledge
- **Void Corruption**: Wielded by VoidLords for power and domination

## Abilities

Flux-attuned individuals can:
- Move objects with their mind
- Sense emotions and intentions
- Predict future events
- Enhance physical abilities
- Communicate telepathically
- Create energy shields

## Training

Young Flux-attuned individuals are taken to the SynthKeeper Sanctuary on Nexaria Prime to begin their training as Initiates under a SynthKeeper Master.
""",

    "02_xarn_velgor.md": """# Xarn Velgor - Supreme VoidLord

Xarn Velgor is one of the most feared VoidLords in the history of the QuantumVerse. Once known as Kael Brightwing, he was a promising SynthKeeper Guardian before falling to the Void Corruption.

## Early Life

Born on Zarathos, Kael showed exceptional talent with Synth Flux from a young age. He was discovered by SynthKeeper Master Theron Vael and trained in the ways of Synth Harmony.

## Fall to Void Corruption

During the Synthetic Wars, Kael's fear of losing his loved ones led him to seek forbidden knowledge. Supreme Archon Malakor manipulated these fears, turning him to the Void Corruption.

## Powers

Xarn Velgor wields immense power:
- Mastery of Void Corruption techniques
- Exceptional skill with Photon Blade combat
- Ability to manipulate others through Synth Flux
- Superhuman strength and reflexes

## Role in Dominion Hegemony

As the Supreme Archon's enforcer, Xarn Velgor leads the Dominion Guards in hunting down remaining SynthKeepers and suppressing the Resistance Coalition.
""",

    "03_photon_blade.md": """# Photon Blade

The Photon Blade is the signature weapon of both SynthKeepers and VoidLords. It consists of a plasma beam contained within an electromagnetic field, powered by Synth Flux.

## Construction

Creating a Photon Blade is a rite of passage for SynthKeeper Initiates. The process involves:
1. Gathering focusing crystals from deep caves
2. Constructing the hilt mechanism
3. Attuning the crystal through Synth Flux meditation
4. Final assembly and testing

## Combat Techniques

There are seven traditional forms of Photon Blade combat:
- Form I: Basic strikes and parries
- Form II: Dueling-focused technique
- Form III: Defensive posture
- Form IV: Acrobatic style
- Form V: Aggressive power attacks
- Form VI: Balanced approach
- Form VII: Mastery of Void Corruption energy

## Colors

The color of a Photon Blade reflects its user's connection to Synth Flux:
- Blue/Green: Traditional SynthKeeper colors (Synth Harmony)
- Red: VoidLord signature (Void Corruption)
- Purple: Rare, indicates mastery of both aspects
- White: Purified crystals, symbol of redemption
- Yellow: SynthKeeper Sentinels
""",

    "04_nexaria_prime.md": """# Nexaria Prime - The Capital World

Nexaria Prime is the political and cultural center of the QuantumVerse. This ecumenopolis (city-planet) is home to trillions of beings from thousands of species.

## Geography

The entire planet is covered in multilevel city structures reaching kilometers into the sky and deep underground.

## Key Locations

### SynthKeeper Sanctuary
The headquarters of the SynthKeeper Order, featuring:
- Training halls for Initiates
- The Archives (vast library of knowledge)
- Council chambers
- Meditation gardens

### Government District
Home to the United Concordat Senate and administrative buildings.

### Industrial Sector
Manufacturing facilities powered by clean fusion reactors.

## History

Nexaria Prime has been the capital for over 25,000 years. During the Dominion Hegemony's rise, the planet fell under military occupation and the SynthKeeper Sanctuary was attacked.
""",

    "05_stellar_hawk.md": """# Stellar Hawk - The Fastest Ship in the Galaxy

The Stellar Hawk is a modified VCX-100 light freighter, famous as "the ship that made the Kessel Run in less than twelve quantum leagues."

## Specifications

- Class: Light freighter
- Length: 34.75 meters
- Hyperdrive: Modified quantum drive (0.5 class)
- Armament: Quad plasma rifle turrets
- Crew: 2 (pilot and co-pilot)
- Passengers: 6
- Cargo capacity: 100 metric tons

## History

Won by Dax Corvain in a card game, the Stellar Hawk became instrumental in the Resistance Coalition's fight against the Dominion Hegemony.

## Modifications

Dax and Grawlak have heavily modified the ship:
- Enhanced quantum drive for faster-than-standard travel
- Upgraded shields
- Hidden cargo compartments (for smuggling)
- Advanced sensor jammers
- Improved weapon systems

## Notable Missions

- Rescue of Sera Veylan from Void Core Station
- Battle of Glacior Prime
- Destruction of the second Void Core Station
""",

    "06_resistance_coalition.md": """# Resistance Coalition

The Resistance Coalition is a military organization dedicated to restoring freedom to the QuantumVerse and defeating the Dominion Hegemony.

## Formation

After the Dominion Hegemony destroyed Celestara and declared martial law, Senator Sera Veylan helped form the Resistance Coalition with other rebel cells.

## Leadership

- Supreme Commander: Former Senator Sera Veylan
- Military Strategist: Dax Corvain
- Chief Engineer: Q7-X9
- Special Operations: Lorn Skyfield

## Bases

The Coalition operates from hidden bases throughout the galaxy:
- Main base on Glacior Prime (ice planet)
- Secondary base on Verdantis moon
- Mobile command ships
- Safe houses on Nexaria Prime

## Strategy

The Coalition employs guerrilla warfare tactics:
- Hit-and-run attacks on Dominion facilities
- Intelligence gathering
- Recruitment of defectors
- Protection of remaining SynthKeepers
- Sabotage of Void Core Station
""",

    "07_void_core_station.md": """# Void Core Station - Ultimate Weapon

The Void Core Station is a massive battle station constructed by the Dominion Hegemony, capable of destroying entire planets.

## Specifications

- Diameter: 160 kilometers
- Population: 1.7 million personnel
- Armament:
  - Superlaser (planet-destroying weapon)
  - 10,000 turbolaser batteries
  - 2,500 plasma rifle batteries
  - 2,500 ion cannons
- Hangar: Space for 7,200 Shadow Interceptors
- Complement: 4 Hegemon Warships

## Design

The station is moon-sized with a focusing dish for its superlaser. Power is generated by a hypermatter reactor at its core.

## Construction

Built in secret above Aquilon, using slave labor from conquered worlds. The project took 20 years to complete.

## Weakness

A small thermal exhaust port leads directly to the reactor. A precise strike there can trigger a chain reaction destroying the entire station.

## Destruction

During the Battle of Verdantis, Lorn Skyfield piloted his Striker-X through the station's trenches and fired photon torpedoes into the exhaust port, destroying the Void Core Station.
""",

    "08_synthkeeper_order.md": """# SynthKeeper Order

The SynthKeeper Order is an ancient organization of Flux-attuned peacekeepers who serve as guardians of justice throughout the QuantumVerse.

## History

Founded over 25,000 years ago, the Order has protected the galaxy through countless conflicts.

## Code

SynthKeepers follow a strict code:
- There is no emotion, there is peace
- There is no ignorance, there is knowledge
- There is no passion, there is serenity
- There is no chaos, there is harmony
- There is no death, there is Synth Flux

## Structure

### SynthKeeper Council
Twelve Masters who lead the Order and make important decisions.

### Ranks
1. Youngling - Children being evaluated
2. Initiate - Student assigned to a Master
3. SynthKeeper Guardian - Fully trained member
4. SynthKeeper Master - May train Initiates
5. Council Member - Order leadership

## Training

Training begins in childhood and takes 15-20 years:
- Physical conditioning
- Synth Flux techniques
- Philosophy and ethics
- Photon Blade combat
- Diplomacy and negotiation
- Galactic history and languages

## Fall

During the Synthetic Wars, Supreme Archon Malakor executed Order 66, commanding Synthetic Soldiers to eliminate all SynthKeepers. Most were killed, with only a handful surviving in hiding.
""",

    "09_supreme_archon_malakor.md": """# Supreme Archon Malakor

Supreme Archon Malakor is the ruler of the Dominion Hegemony and the most powerful VoidLord in the QuantumVerse.

## Identity

Malakor was secretly Senator Sheev from Seravelle, who manipulated galactic politics for decades while hiding his true nature as a VoidLord Master.

## Rise to Power

Through careful manipulation:
1. Engineered the Synthetic Wars conflict
2. Gained emergency powers as Supreme Chancellor
3. Eliminated the SynthKeeper Order
4. Declared himself Supreme Archon
5. Transformed the United Concordat into the Dominion Hegemony

## Powers

Mastery of Void Corruption makes Malakor nearly unstoppable:
- Flux lightning (powerful electrical attacks)
- Mind manipulation on a massive scale
- Precognition and battle meditation
- Immortality techniques
- Essence transfer (can possess other bodies)

## Personality

Malakor is patient, calculating, and absolutely ruthless. He views all beings as tools to be used or obstacles to be eliminated.

## Downfall

Ultimately defeated when Xarn Velgor, redeemed by his son Lorn's love, threw Malakor into the reactor core of the second Void Core Station.
""",

    "10_zarathos.md": """# Zarathos - The Desert Planet

Zarathos is a harsh desert world on the Outer Rim, known for its twin suns and dangerous wildlife.

## Geography

- Terrain: Desert, rocky badlands, salt flats
- Climate: Extremely hot days, cold nights
- Water: Moisture farming required for survival
- Moons: 3 small moons

## Inhabitants

### Sand Nomads
Fierce warriors who live in the desert, known for their distinctive breathing apparatus and territorial nature.

### Scavs
Small scavengers who collect and sell scrap technology and droids.

### Moisture Farmers
Settlers who extract water from the atmosphere using vaporators.

## Locations

### Mos Eisley
A spaceport described as "a wretched hive of scum and villainy" where smugglers and criminals gather.

### Anchorhead
A small settlement where moisture farmers trade supplies.

### Beggar's Canyon
A popular location for racing velocity riders through narrow rock formations.

## History

Zarathos was the birthplace of both Kael Brightwing (later Xarn Velgor) and his son Lorn Skyfield. It remained largely ignored by the Dominion Hegemony until they searched for the plans to Void Core Station.
""",

    "11_grawlak.md": """# Grawlak - Loyal Co-Pilot

Grawlak is a Graxx warrior and co-pilot of the Stellar Hawk, serving as Dax Corvain's closest friend and ally.

## Species: Graxx

Graxx are tall, strong beings covered in fur, native to the forest planet Kashyyyk. Known for:
- Exceptional strength and durability
- Fierce loyalty to friends
- Skill with weapons and technology
- Long lifespan (400+ years)
- Complex language (Shyriiwook)

## Background

Grawlak was enslaved by the Dominion Hegemony but rescued by Dax during a smuggling run. He swore a life debt to Dax and has been his partner ever since.

## Skills

- Expert mechanic and engineer
- Skilled pilot and navigator
- Proficient with plasma rifles and crossbows
- Hand-to-hand combat expert

## Personality

Despite his fearsome appearance, Grawlak is:
- Gentle with friends
- Fiercely protective of allies
- Honorable and ethical
- Sometimes quick to anger when provoked

## Role in Resistance

Grawlak serves as:
- Co-pilot and mechanic of Stellar Hawk
- Heavy weapons specialist
- Demolitions expert
- Diplomatic liaison with Graxx colonies
""",

    "12_sera_veylan.md": """# Sera Veylan - Leader of the Resistance

Sera Veylan is a former Senator from Celestara who became one of the leaders of the Resistance Coalition against the Dominion Hegemony.

## Early Life

Born into Celestara's royal family, Sera was raised with strong ethical values and trained in diplomacy, leadership, and self-defense.

## Political Career

As Senator, she:
- Advocated for peaceful solutions
- Opposed Supreme Archon Malakor's militarization
- Secretly supported resistance movements
- Helped preserve data about Void Core Station

## Personal Tragedy

The Dominion destroyed Celestara as a demonstration of the Void Core Station's power, killing billions including her family. This traumatic event strengthened her resolve to fight tyranny.

## Leadership Style

Sera leads through:
- Inspirational speeches
- Strategic planning
- Diplomatic negotiations
- Personal courage in battle

## Skills

- Expert diplomat and negotiator
- Skilled with plasma rifles
- Basic pilot training
- Synth Flux sensitivity (untrained)
- Fluent in multiple languages

## Relationship with Resistance

She coordinated multiple rebel cells into the unified Resistance Coalition and secured critical funding and equipment.
""",

    "13_theron_vael.md": """# Theron Vael - The Wise Master

Theron Vael was a legendary SynthKeeper Master known for his wisdom and combat prowess.

## Early Years

Discovered as a young Flux-attuned child on the planet Stewjon, Theron was trained at the SynthKeeper Sanctuary and eventually became one of the Order's most respected Masters.

## Accomplishments

- Defeated VoidLord Vex Shadowborn
- Trained Kael Brightwing (later Xarn Velgor)
- Served on the SynthKeeper Council
- Negotiated peace in numerous conflicts
- Master of Photon Blade Form III (defensive)

## Philosophy

Theron believed in:
- Patience and understanding
- The primacy of knowledge over aggression
- Redemption for those who have fallen
- Living in harmony with Synth Flux

## Sacrifice

When Order 66 was executed, Theron helped other SynthKeepers escape but was killed defending the SynthKeeper Sanctuary. Before dying, he became one with Synth Flux, learning to manifest as a spirit to guide future generations.

## Legacy

As a Synth Flux spirit, Theron continued to mentor:
- Lorn Skyfield in the ways of SynthKeepers
- Providing wisdom during critical battles
- Teaching the technique of immortality through Synth Flux

His teachings emphasized that Synth Flux is not just power, but understanding and compassion.
""",

    "14_zyrax.md": """# Zyrax - Grand Master

Zyrax is a legendary SynthKeeper Grand Master, renowned as one of the most powerful and wise Flux users in history.

## Appearance

- Species: Ancient Flux-evolved being
- Height: 66 centimeters
- Age: Over 900 years
- Distinctive green skin and pointed ears
- Walks with a gimer stick

## Philosophy

Zyrax is known for cryptic wisdom:
- "Do or do not. There is no try."
- "Fear is the path to Void Corruption."
- "Size matters not. Judge me by my size, do you?"
- "Wars not make one great."

## Powers

Despite small stature, Zyrax possesses extraordinary abilities:
- Exceptional Photon Blade skills
- Profound Synth Flux manipulation
- Precognition and wisdom
- Ability to lift massive objects
- Lightning-fast reflexes

## Teaching

Lived in exile on Myrkvale after the fall of the SynthKeeper Order, where he trained Lorn Skyfield in advanced techniques.

Training methods included:
- Physical challenges in swamp environment
- Mental discipline exercises
- Unlearning limiting beliefs
- Deep connection with living Synth Flux

## Death and Legacy

At age 900, Zyrax peacefully became one with Synth Flux, but promised to remain as a guiding spirit. His final words emphasized that the Synth Flux would be with Lorn always.
""",

    "15_dax_corvain.md": """# Dax Corvain - Smuggler and Hero

Dax Corvain is a smuggler, pilot, and captain of the Stellar Hawk who became a key leader in the Resistance Coalition.

## Background

Born on Corellia, Dax grew up street-smart and independent. He entered the smuggling business young, earning a reputation for:
- Completing impossible runs
- Quick thinking under pressure
- Charming his way out of trouble
- Outstanding piloting skills

## Personality

- Cocky and confident exterior
- Hidden heart of gold
- Loyal to friends
- Skeptical of Synth Flux ("hokey religions")
- Motivated by credits but will do the right thing

## Skills

- Expert pilot (one of the best in the galaxy)
- Quick-draw with plasma rifles
- Skilled negotiator and liar
- Knows criminal underworld
- Basic mechanical knowledge

## Character Development

Initially motivated by money, Dax evolved:
1. Reluctantly helped rescue Sera
2. Stayed for the reward
3. Returned to save Lorn at crucial moment
4. Committed fully to Resistance
5. Became General in Resistance forces

## Relationships

- Best friend: Grawlak (co-pilot)
- Romance: Sera Veylan
- Mentor figure: To Lorn Skyfield
- Rival: Various bounty hunters and smugglers

## Famous Quote

"Never tell me the odds!"
""",

    "16_synthetic_soldiers.md": """# Synthetic Soldiers

Synthetic Soldiers were genetically engineered warriors created to serve the United Concordat during the Synthetic Wars.

## Creation

Grown on Aquilon using advanced cloning technology:
- Template: Jango Fett, legendary bounty hunter
- Growth acceleration: 10 years to maturity in 2 years
- Mental conditioning: Obedience and loyalty
- Combat training: From "birth"

## Characteristics

- Identical physical appearance
- White armor with colored markings (unit designation)
- Superior combat abilities
- Unwavering loyalty to command structure
- Limited independent thinking

## Units

Different specializations:
- Standard Infantry
- Heavy Weapons Specialists
- Snipers
- Pilots
- ARF (Advanced Recon Force)
- Commandos (elite special operations)

## Order 66

Supreme Archon Malakor embedded a secret protocol in all Synthetic Soldiers. When activated:
- Commanded them to eliminate all SynthKeepers
- Treated SynthKeepers as traitors
- Led to near-extinction of SynthKeeper Order

## Transition to Dominion Guards

After the Synthetic Wars, Synthetic Soldiers were replaced with recruited Dominion Guards as the clone facilities were shut down.
""",

    "17_dominion_guards.md": """# Dominion Guards

Dominion Guards are the elite soldiers of the Dominion Hegemony, recognizable by their distinctive white armor.

## Organization

Divided into legions:
- 501st Legion (Xarn Velgor's Fist)
- Death Troopers (elite special forces)
- Scout Troopers (reconnaissance)
- Snowtroopers (cold environment)
- Shoretroopers (coastal defense)

## Equipment

- White plastoid armor (some thermal protection)
- E-11 plasma rifle (standard issue)
- Thermal detonators
- Communication equipment
- Environmental gear as needed

## Training

Recruited from across the Dominion:
- Intensive combat training
- Ideological conditioning
- Weapons proficiency
- Unit tactics
- Loyalty enforcement

## Effectiveness

Despite reputation, Dominion Guards have weaknesses:
- Armor doesn't provide full protection
- Helmets limit visibility
- Training emphasizes obedience over initiative
- Often overconfident due to numerical superiority

## Notable Units

**Death Troopers**: Elite all-black armor, enhanced training, serve as guards for high-value targets and commanders.
""",

    "18_shadow_interceptors.md": """# Shadow Interceptors

Shadow Interceptors are the Dominion Hegemony's primary starfighter, recognizable by their distinctive angular design.

## Design Philosophy

Emphasizes:
- Speed and maneuverability
- Cost-effectiveness (mass production)
- Intimidation through distinctive engine sound
- Expendability of pilots

## Variants

**TIE/LN (Standard)**
- Twin ion engines
- No shields
- No hyperdrive
- Limited life support
- Weapons: Twin plasma cannons

**TIE/IN Interceptor**
- Faster and more maneuverable
- Improved weapons
- Still no shields

**TIE/SA Bomber**
- Carries torpedoes and bombs
- Slower but heavily armed

**TIE/D Defender**
- Shields and hyperdrive
- Most advanced variant
- Limited production

## Tactics

Deployed in swarms:
- Overwhelming numbers
- Formation flying
- Hit-and-run attacks
- Coordination with Hegemon Warships

## Weaknesses

- No shields (vulnerable to single hit)
- Limited range without carrier
- Pilots expendable in Dominion doctrine
- Poor visibility from cockpit
""",

    "19_striker_x_fighter.md": """# Striker-X Fighter

The Striker-X is the primary fighter of the Resistance Coalition, known for its distinctive S-foil wings that split into attack position.

## Specifications

- Length: 12.5 meters
- Crew: 1 pilot + 1 astromech synthetic
- Armament: 4 plasma cannons, 2 proton torpedo launchers
- Shields: Deflector shield generator
- Hyperdrive: Class 1

## Design Features

**S-Foils**: Split into attack position for better weapon coverage and heat dissipation, or close for atmospheric flight and landing.

**Astromech Integration**: R-series synthetic plugs into ship for:
- Navigation calculations
- System repairs
- Combat assistance
- Quantum drive operations

## Combat Role

- Space superiority fighter
- Escort missions
- Planetary assault
- Trench runs (precision targeting)

## Notable Pilots

- Lorn Skyfield (Red Five)
- Wedge Antilles (Red Two)
- Biggs Darklighter (Red Three)

## Famous Battle

The Striker-X proved decisive at the Battle of Verdantis, where Lorn Skyfield used one to destroy the Void Core Station.

## Advantages Over Shadow Interceptors

- Shields provide survivability
- Hyperdrive allows independent operations
- Superior weapons
- Better targeting systems
- Pilot support from astromech
""",

    "20_titan_walker.md": """# Titan Walker - All Terrain Armored Transport

The Titan Walker is a massive quadrupedal combat vehicle used by the Dominion Hegemony for ground assault.

## Specifications

- Height: 22.5 meters
- Length: 20 meters
- Crew: 5 (pilot, gunner, commander, 2 engineers)
- Capacity: 40 Dominion Guards
- Armament:
  - 2 heavy plasma cannons (head-mounted)
  - 2 medium plasma cannons
- Armor: Heavy reinforced plating

## Design

Four-legged walking design provides:
- Ability to traverse rough terrain
- Height advantage over infantry
- Intimidation factor
- Stable firing platform

## Deployment

Used for:
- Ground assault operations
- Garrison intimidation
- Urban pacification
- Planetary occupation

## Weaknesses

- Slow movement speed
- Vulnerable underside
- Exposed neck joint
- Can be tripped by cable weapons

## Notable Engagements

**Battle of Glacior Prime**: Titan Walkers led the assault on the Resistance base but were ultimately defeated through:
- Snowspeeder cable attacks
- Photon Blade strikes to legs
- Plasma rifle concentration on neck joint

The walker's imposing appearance makes it a symbol of Dominion oppression.
""",

    "21_q7_x9_synthetic.md": """# Q7-X9 - Astromech Synthetic

Q7-X9 is a resourceful astromech synthetic who has served in numerous adventures and battles throughout the QuantumVerse.

## Specifications

- Model: R2-series astromech
- Height: 1.09 meters
- Locomotion: Wheeled treads, rocket boosters (sometimes)
- Color: Blue and white plating

## Capabilities

**Technical**:
- Starship repair and maintenance
- Computer system infiltration
- Holographic projection
- Data storage and retrieval
- Quantum drive calculations
- Electronic communication

**Tools**:
- Extending manipulator arms
- Arc welder
- Circular saw
- Periscope
- Fire extinguisher
- Oil injector

## Personality

Despite being synthetic, Q7 exhibits:
- Courage and loyalty
- Stubbornness
- Tendency to beep sassily
- Problem-solving creativity
- Protective of friends

## History

- Served Queen Amidala of Seravelle
- Partnered with Kael Brightwing during Synthetic Wars
- Became Lorn Skyfield's companion
- Critical role in destroying both Void Core Stations
- Stored complete plans for Void Core Station

## Relationship with P-5YN

Best friend/constant argument partner with protocol synthetic P-5YN. Their banter provides comic relief during tense missions.

## Heroic Moments

- Repairing Sera's ship under fire
- Delivering Void Core plans to Resistance
- Hacking Dominion systems
- Fixing Lorn's Striker-X during battles
""",

    "22_p_5yn_protocol_synthetic.md": """# P-5YN - Protocol Synthetic

P-5YN is a humanoid protocol synthetic specializing in diplomatic relations, translation, and etiquette.

## Specifications

- Model: 3PO-series protocol synthetic
- Height: 1.67 meters
- Plating: Gold-colored metal
- Build: Humanoid with visible mechanical joints

## Functions

**Primary**: Translation and cultural interpretation
- Fluent in over 6 million forms of communication
- Expert on cultural customs and protocols
- Diplomatic advisor
- Etiquette instruction

**Secondary**: Minor repairs, data analysis, record-keeping

## Personality

P-5YN is characterized by:
- Constant worry and anxiety
- Formal speech patterns
- Rule-following nature
- Loyalty to masters
- Frequent complaints about odds
- Deep concern for Q7-X9's safety

## Famous Quotes

- "We're doomed!"
- "I suggest a new strategy, Q7: let the Graxx win."
- "Sir, the possibility of successfully navigating an asteroid field is approximately 3,720 to 1!"
- "I am fluent in over six million forms of communication."

## History

- Built on Zarathos by Kael Brightwing as a child
- Served Sera Veylan's family on Celestara
- Accompanied Resistance Coalition throughout conflict
- Translated for various alien species
- Helped coordinate Battle of Verdantis

## Relationship with Organics

Despite anxiety, P-5YN shows genuine care for:
- Sera (whom he serves loyally)
- Lorn (whom he remembers building him)
- Dax and Grawlak (though he finds them crude)
- Q7 (best friend, despite constant bickering)
""",

    "23_synthetic_wars.md": """# The Synthetic Wars

The Synthetic Wars was a galaxy-wide conflict that lasted three years and resulted in the fall of the SynthKeeper Order and rise of the Dominion Hegemony.

## Causes

**Political**:
- Growing corruption in United Concordat Senate
- Outer Rim worlds feeling underrepresented
- Trade disputes and taxation of routes
- Corporate influence over government

**Hidden Manipulation**:
- Supreme Archon Malakor (as Senator Sheev) orchestrated both sides
- Used conflict to gain emergency powers
- Planned to eliminate SynthKeepers
- Goal: Transform Concordat into Dominion

## Key Events

### Year 1: Outbreak
- Breakaway Syndicate formed by dissatisfied systems
- First Battle of Geonosis
- SynthKeepers became generals of Synthetic Soldier armies
- Massive military buildup on both sides

### Year 2: Escalation
- Thousands of battles across the galaxy
- SynthKeeper Sanctuary raided multiple times
- Economic strain on both governments
- Growing war weariness

### Year 3: Conclusion
- Xarn Velgor (Kael) falls to Void Corruption
- Order 66 executed - Synthetic Soldiers kill SynthKeepers
- Malakor reveals himself as Supreme Archon
- United Concordat becomes Dominion Hegemony
- Breakaway Syndicate leaders assassinated
- Peace through tyranny established

## Casualties

- Billions of civilians dead
- Most SynthKeepers eliminated
- Thousands of worlds devastated
- Economic collapse in many systems

## Legacy

The war achieved Malakor's goals:
- SynthKeeper Order destroyed
- Democracy replaced with dictatorship
- Population fearful and compliant
- Military industrial complex empowered
- Foundation for Void Core Station construction

The few surviving SynthKeepers went into hiding, and the galaxy entered a dark age lasting 20+ years until the Resistance Coalition formed.
""",

    "24_quantum_drive_technology.md": """# Quantum Drive Technology

Quantum drive allows starships to travel faster than light through quantum tunneling space, making interstellar travel practical.

## Principles

**Quantum Tunneling**: Ships don't move through normal space, but tunnel through an alternate dimension where physics work differently, allowing apparent FTL travel.

**Navigation**: Complex calculations required to avoid:
- Gravity wells (can pull ship out of quantum space)
- Asteroid fields
- Other ships
- Spatial anomalies

## Drive Classes

Rating indicates relative speed:
- Class 0.5: Fastest (modified, very rare)
- Class 1: Military standard
- Class 2: Civilian fast
- Class 3-4: Commercial average
- Class 6+: Slow freighters

Lower number = faster speed

## Components

**Hypermatter Reactor**: Provides enormous energy needed

**Field Generator**: Creates quantum tunnel effect

**Navigation Computer**: Calculates safe routes

**Motivator**: Initiates jump

## Safety Features

- Gravity well detection (prevents jumping near planets)
- Collision sensors
- Emergency shutoff
- Backup power systems

## Notable Drives

**Stellar Hawk's Drive**: Modified Class 0.5, illegally enhanced, can outrun Hegemon Warships but prone to breaking down

## Limitations

- Can't jump from within gravity wells
- Requires clear route calculation
- Fuel intensive
- Expensive to maintain
- Mass affects speed

## In Combat

Usually can't be used during battle due to:
- Enemy ships preventing calculation time
- Tractor beams
- Interdiction fields
- Need to escape gravity effects
""",

    "25_hegemon_warship.md": """# Hegemon Warship - Star Destroyer

The Hegemon Warship is the Dominion Hegemony's primary capital ship, a massive dagger-shaped vessel that represents imperial might.

## Specifications

- Class: Star Destroyer
- Length: 1,600 meters
- Crew: 37,000 officers and enlisted
- Troops: 9,700 Dominion Guards
- Starfighters: 72 Shadow Interceptors
- Ground vehicles: 20 Titan Walkers, 30 Scout Walkers

## Armament

- 60 turbolaser batteries
- 60 ion cannons
- 10 tractor beam projectors
- 8 torpedo launchers

## Role

**Space Superiority**: Overwhelm enemy ships through firepower and fighter deployment

**Planetary Occupation**: Deploy ground forces and provide orbital bombardment

**Blockade**: Prevent ships from leaving/entering systems

**Intimidation**: Psychological weapon through sheer size

## Design Philosophy

- Wedge shape for forward firepower concentration
- Bridge tower (vulnerable but commanding view)
- Massive engines for size/speed ratio
- Heavy armor plating
- Redundant systems

## Tactics

Typically deployed as:
- Flagship of battle groups
- Sector patrol vessels
- Blockade enforcers
- Show of force for subjugation

## Weaknesses

- Vulnerable bridge tower
- Poor rear defense
- Requires massive crew
- Expensive to build/maintain
- Slow to maneuver

## Notable Ships

- **Devastator**: Xarn Velgor's flagship
- **Executor**: Super-sized variant, 19,000 meters
- **Chimaera**: Grand Admiral Thrawn's ship
""",

    "26_verdantis_battle.md": """# Battle of Verdantis

The Battle of Verdantis was the decisive conflict that destroyed the first Void Core Station and gave the Resistance Coalition its first major victory.

## Background

The Resistance discovered the Void Core Station's weakness - a small thermal exhaust port leading to the main reactor. Plans stolen by agents (delivered by Q7-X9) showed the vulnerability.

## Resistance Forces

- 30 Striker-X fighters
- 15 Striker-Y bombers
- Support ships
- Ground teams on Verdantis moon

## Dominion Defense

- Void Core Station itself
- 100+ Shadow Interceptors
- Multiple Hegemon Warships
- Defensive turbolaser batteries

## Battle Phases

### Phase 1: Initial Assault
- Resistance fighters engaged Shadow Interceptors
- Drew defenders away from station
- Bombers attempted surface runs

### Phase 2: Trench Run
- Fighters dove into surface trench
- Heavy casualties from defensive fire
- Multiple failed attempts at exhaust port

### Phase 3: Lorn's Run
- Lorn Skyfield in Red Five
- Used Synth Flux to guide shot
- Fired proton torpedoes at exact moment
- Direct hit on exhaust port

### Phase 4: Destruction
- Chain reaction through reactor
- Evacuation attempts failed
- Station exploded completely
- Resistance escaped before shockwave

## Casualties

**Resistance**: 20 fighters lost, approximately 30 pilots

**Dominion**:
- 1.7 million personnel on station
- Dozens of Shadow Interceptors
- Supreme Archon Malakor survived

## Significance

- Proved Dominion could be defeated
- Boosted Resistance morale galaxy-wide
- New recruits joined Resistance
- Demonstrated SynthKeeper abilities
- Forced Dominion to begin second station

## Aftermath

- Lorn Skyfield became hero
- Dax and Grawlak received medals
- Sera coordinated expanded resistance efforts
- Dominion began more aggressive campaigns
- Second Void Core Station construction accelerated
""",

    "27_vanguard_sentinels.md": """# Vanguard Sentinels

Vanguard Sentinels are elite warriors from the planet Vanguard Prime, known for their distinctive armor and strict honor code.

## Culture

**The Way**: Ancient code of honor emphasizing:
- Strength and combat prowess
- Honor above all
- Loyalty to clan and comrades
- Self-reliance
- Tradition and heritage

**Armor**: Sacred, passed through generations
- Made of beskar (nearly indestructible metal)
- Never removed in front of others
- Decorated with clan symbols
- Represents identity

## Training

From childhood:
- Combat with all weapons
- Survival skills
- Tracking and hunting
- Piloting
- Tactics and strategy
- The Way's philosophy

## Equipment

**Weapons**:
- Plasma rifles
- Wrist-mounted rockets
- Grappling cables
- Vibroblades
- Various explosives

**Armor Features**:
- Beskar plating (deflects even Photon Blades)
- Helmet with HUD and sensors
- Jetpack for aerial mobility
- Environmental seals

## History with Dominion

- Originally independent warriors
- Some served as bounty hunters
- Vanguard Prime occupied by Dominion
- Many joined Resistance after occupation
- Others remained neutral or worked as mercenaries

## Notable Sentinels

**Jango Fett**: Template for Synthetic Soldiers

**Boba Fett**: Bounty hunter, clone of Jango

**Din Djarin**: Foundling who helped protect a Flux-sensitive child

## Code of Honor

- A warrior's word is absolute
- Protect the helpless
- Teach the young The Way
- Never break a contract
- Death before dishonor
""",

    "28_breakaway_syndicate.md": """# Breakaway Syndicate

The Breakaway Syndicate was a coalition of star systems that attempted to secede from the United Concordat, sparking the Synthetic Wars.

## Formation

**Grievances**:
- Over-taxation of trade routes
- Under-representation in Senate
- Corporate control of government
- Corruption in Nexaria Prime
- Neglect of Outer Rim worlds

**Leadership**:
- Count Dooku (Lord Tyraxis) - former SynthKeeper
- Trade Federation leaders
- Corporate Alliance representatives
- Banking Clan financiers

## Member Systems

Thousands of systems including:
- Geonosis (military manufacturing)
- Seravelle (Queen Amidala's world)
- Various Outer Rim colonies
- Corporate-controlled sectors

## Military

**Combat Synthetic Army**:
- Battle Synthetics (droids)
- Super Battle Synthetics
- Destroyer Synthetics
- Vulture fighters
- Thousands of warships

**Advantages**:
- No living casualties
- Rapid production
- Fearless in combat
- Coordinated via central control

**Weaknesses**:
- Vulnerable to central control destruction
- Limited initiative
- Predictable tactics

## The Conspiracy

Unknown to most Syndicate members:
- Secretly controlled by Supreme Archon Malakor
- Entire war was orchestrated
- Leaders manipulated on both sides
- Goal was never actual independence
- Planned to be betrayed once SynthKeepers eliminated

## Collapse

At war's end:
- Combat Synthetic armies shut down
- Leadership assassinated
- Member systems forcibly re-integrated
- Assets seized by Dominion
- Became example of "rebellion's futility"

## Legacy

The Breakaway crisis was manufactured, but legitimate grievances that sparked it remained unaddressed, eventually leading to formation of the Resistance Coalition decades later.
""",

    "29_flux_abilities_advanced.md": """# Advanced Synth Flux Abilities

Beyond basic Flux manipulation, SynthKeeper Masters and VoidLords can develop extraordinary abilities.

## Defensive Techniques

**Flux Barrier**: Create protective shield
- Deflects plasma fire
- Can stop physical objects
- Requires concentration
- Drains stamina with sustained use

**Battle Meditation**: Enhance allies' abilities
- Boost morale and coordination
- Share tactical insights
- Extend reflexes to entire fleet
- Very rare ability

**Tutaminis**: Absorb and dissipate energy
- Catch plasma bolts
- Absorb Flux lightning
- Redirect energy attacks
- Requires mastery

## Offensive Techniques

**Flux Push/Pull**: Telekinetic force
- Throw opponents
- Crush objects
- Disable weapons
- Pull items to hand

**Flux Lightning** (Void Corruption):
- Electrical attack from fingertips
- Causes intense pain
- Can kill at high power
- Signature VoidLord technique

**Mind Trick**: Influence weak-minded
- Suggestion and persuasion
- Memory alteration (advanced)
- Cannot affect strong-willed individuals

## Sensory Abilities

**Precognition**: See possible futures
- Visions during sleep
- Combat foresight (reflexes)
- Varies in clarity
- Future always in motion

**Flux Sense**: Detect disturbances
- Feel presence of others
- Sense emotions and intentions
- Detect danger
- Varies by user's connection

**Psychometry**: Read object histories
- Learn from touching items
- See past events
- Varies in detail
- Emotionally intense memories easier

## Master-Level Skills

**Flux Healing**: Accelerate recovery
- Heal wounds
- Cure poisons
- Exhausting to perform
- Cannot heal oneself well

**Beast Control**: Influence animal minds
- Calm aggressive creatures
- Ride untamed beasts
- Coordinate animal actions
- Requires empathy

**Immaterial Form**: Become Flux spirit
- Only after death
- Requires training
- Can manifest to living
- Achieved by Theron, Zyrax, Kael

## Forbidden Techniques

**Flux Drain**: Steal life energy
- Siphon vitality from victims
- Extends own life
- Extremely dark technique
- Corrupts user

**Essence Transfer**: Possess other bodies
- Cheat death
- Requires host
- Ultimate Void Corruption
- Malakor's goal
""",

    "30_resistance_vehicles.md": """# Resistance Coalition Vehicles

The Resistance uses various vehicles adapted from civilian and captured military hardware.

## Starfighters

**Striker-X Fighter**:
- Primary space superiority fighter
- S-foil wings for attack mode
- Astromech synthetic integration
- Shields and hyperdrive

**Striker-Y Bomber**:
- Heavy assault craft
- Ion cannons and torpedo launchers
- Slower but heavily armed
- Used for capital ship attacks

**Striker-A Interceptor**:
- Fastest Resistance fighter
- Minimal shields, maximum speed
- Hit-and-run tactics
- Reconnaissance missions

## Ground Vehicles

**Snowspeeder**:
- Modified civilian airspeeder
- Adapted for cold environments
- Harpoon and tow cable
- Used to trip Titan Walkers
- Two crew: pilot and gunner

**T-47 Airspeeder**:
- Civilian atmospheric craft
- Repulsorlift propulsion
- Armed with plasma cannons
- Used on various terrain types

## Transports

**GR-75 Transport**:
- Medium cargo ship
- Carries troops and equipment
- Lightly armed
- Modular cargo configuration

**Corvette CR90**:
- Diplomatic ship
- Fast blockade runner
- Turbolasers for defense
- Versatile command ship

## Captured Equipment

**AT-ST Scout Walkers**:
- Captured from Dominion
- Two-legged walker
- Reconnaissance and patrol
- Reprogrammed for Resistance use

**Shadow Interceptors**:
- Occasionally captured intact
- Used for infiltration
- Requires constant maintenance
- No hyperdrive limits usefulness

## Modifications

Resistance mechanics constantly improvise:
- Enhanced weapons
- Improved shields
- Better sensors
- Recycled parts from multiple sources
- Creative repairs with limited resources

The Resistance motto for vehicles: "Keep it flying, no matter how."
""",

    "31_galactic_currency.md": """# Quantum Credits and Economy

The primary currency across the QuantumVerse is the quantum credit, a digital currency system.

## Currency Types

**Republic/Dominion Credits**: Standard across most of galaxy
- Digitally tracked
- Accepted almost everywhere
- Backed by galactic governments
- Secure against counterfeiting

**Local Currencies**: Some worlds maintain own systems
- Wupiupi (Zarathos)
- Truguts (various Outer Rim)
- Often at disadvantageous exchange rates

**Physical Credits**: Rare but exist
- Credit chips
- Ingots for large amounts
- Used where digital systems unreliable
- Easier to steal or counterfeit

## Economic Systems

**Core Worlds**: Advanced post-scarcity
- Most needs met by technology
- Credits used for luxury goods
- Service economy dominant
- High living standards

**Mid Rim**: Mixed economy
- Manufacturing and agriculture
- Credits essential for trade
- Middle-class standard of living
- Some poverty in industrial areas

**Outer Rim**: Frontier economy
- Resource extraction
- Self-sufficiency important
- Credits scarce
- Barter common in remote areas

## Under the Dominion

**Economic Control**:
- Taxation increased dramatically
- Resources redirected to military
- Worlds conquered had assets seized
- Resistance forces economic disruption

**Black Markets**: Thrived under occupation
- Smuggling increased
- Illegal goods trade
- Resistance funded partly through crime
- Bribes commonplace

## Cost of Living

**Typical Prices** (in credits):

Starship fuel: 100-1000 per fill
Decent meal: 5-10
Hotel room: 30-100 per night
Plasma rifle: 500-2000
Basic starship: 25,000-100,000
Used speeder: 2,000-5,000
Bribe for minor official: 50-200

**Smuggler Rates**: Varied widely
- Dax charged 17,000 for Alderaan run
- Dangerous routes commanded premium
- Payment often negotiable

## Wealth Inequality

Huge disparity between:
- Corporate executives and aristocracy (billions)
- Middle class (comfortable but limited)
- Poor and slaves (subsistence or nothing)

The Dominion increased inequality through:
- Military spending
- Corruption
- Confiscation of property
- Forced labor
""",

    "32_species_diversity.md": """# Species of the QuantumVerse

The galaxy contains thousands of sentient species, each with unique characteristics.

## Major Species

### Humans
- Most numerous and widespread
- Adaptable to many environments
- No special abilities
- Dominant in government and military

### Graxx (Wookiees)
- Tall, strong, fur-covered
- Exceptional strength
- Long-lived (400+ years)
- Honor-based culture
- Home: Kashyyyk (forest planet)

### Twileks
- Distinctive head-tails (lekku)
- Various skin colors
- Often enslaved (unfortunately)
- Skilled dancers and negotiators
- Home: Ryloth

### Rodians
- Green skin, large eyes
- Natural hunters
- Many became bounty hunters
- Violent reputation
- Home: Rodia

### Mon Calamari
- Amphibious species
- Bulbous eyes
- Excellent ship designers
- Key Resistance leaders
- Home: Mon Cala

### Bothans
- Fur-covered, canine-like
- Expert spies and intelligence agents
- Information brokers
- Politically influential
- "Many Bothans died..." (famous sacrifice)

## Lesser-Known Species

### Scavs (Jawas)
- Small scavengers
- Hidden faces, glowing eyes
- Technology traders
- Clan-based society
- Home: Zarathos

### Sand Nomads (Tusken Raiders)
- Masked desert warriors
- Territorial and aggressive
- Traditional weapons and banthas
- Mistrusted by settlers
- Home: Zarathos deserts

### Fennix (Ewoks)
- Small, fur-covered teddy-bear appearance
- Primitive technology
- Deceptively dangerous warriors
- Forest dwellers
- Home: Verdantis moon

### Vorgans (Hutts)
- Massive slug-like beings
- Criminal enterprise leaders
- Extremely long-lived
- Resistant to Flux mind tricks
- Home: Nal Hutta

## Synth Flux Sensitivity

All species can potentially be Flux-attuned:
- Humans: Most common SynthKeepers
- Others: Various species in SynthKeeper Order
- No species has universal sensitivity
- Born, not made (though training develops it)

## Language

**Galactic Basic**: Common language (similar to English)
- Understood across most of galaxy
- Used in Senate, military, trade
- Most species can speak it

**Species Languages**: Maintained alongside Basic
- Shyriiwook (Graxx)
- Binary (Synthetics)
- Huttese (Criminal underworld)
- Countless others

## Discrimination

**Under Dominion**:
- Human-centric policies
- Non-humans faced discrimination
- Graxx enslaved
- Alien species restricted from certain positions

**In Resistance**:
- Inclusive of all species
- United against tyranny
- Diversity seen as strength
"""
}

# Создаем все документы
output_dir = Path("knowledge_base")
output_dir.mkdir(exist_ok=True)

for filename, original_content in documents.items():
    # Заменяем термины
    modified_content = replace_terms(original_content, terms_map)

    # Сохраняем файл
    filepath = output_dir / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(modified_content)

    print(f"Created: {filename}")

print(f"\nSuccessfully created {len(documents)} documents in knowledge_base/")
print("Terms have been replaced according to terms_map.json")
