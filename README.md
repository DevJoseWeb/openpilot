Community Port information
======

This is the "Community Port" for Kia and Hyundai.
[openpilot](http://github.com/commaai/openpilot) is an open source driving agent. Currently, it performs the functions of Adaptive Cruise Control (ACC) and Lane Keeping Assist System (LKAS) for selected Honda, Toyota, Acura, Lexus, Chevrolet, Hyundai, Kia. It's about on par with Tesla Autopilot and GM Super Cruise, and better than [all other manufacturers](http://www.thedrive.com/tech/5707/the-war-for-autonomous-driving-part-iii-us-vs-germany-vs-japan).

The openpilot codebase has been written to be concise and to enable rapid prototyping. We look forward to your contributions - improving real vehicle automation has never been easier.

Table of Contents
=======

* [Community](#community)
* [Hardware](#hardware)
* [Supported Cars](#supported-cars)
* [Community Maintained Cars](#community-maintained-cars)
* [In Progress Cars](#in-progress-cars)
* [How can I add support for my car?](#how-can-i-add-support-for-my-car)
* [Directory structure](#directory-structure)
* [User Data / chffr Account / Crash Reporting](#user-data--chffr-account--crash-reporting)
* [Testing on PC](#testing-on-pc)
* [Contributing](#contributing)
* [Licensing](#licensing)

---

Community
------

openpilot is developed by [comma.ai](https://comma.ai/) and users like you.

We have a [Twitter you should follow](https://twitter.com/comma_ai).

Also, we have a several thousand people community on [Discord](https://discord.comma.ai).

<table>
  <tr>
    <td><a href="https://www.youtube.com/watch?v=ICOIin4p70w" title="YouTube" rel="noopener"><img src="https://i.imgur.com/gBTo7yB.png"></a></td>
    <td><a href="https://www.youtube.com/watch?v=1zCtj3ckGFo" title="YouTube" rel="noopener"><img src="https://i.imgur.com/gNhhcep.png"></a></td>
    <td><a href="https://www.youtube.com/watch?v=Qd2mjkBIRx0" title="YouTube" rel="noopener"><img src="https://i.imgur.com/tFnSexp.png"></a></td>
    <td><a href="https://www.youtube.com/watch?v=ju12vlBm59E" title="YouTube" rel="noopener"><img src="https://i.imgur.com/3BKiJVy.png"></a></td>
  </tr>
  <tr>
    <td><a href="https://www.youtube.com/watch?v=Z5VY5FzgNt4" title="YouTube" rel="noopener"><img src="https://i.imgur.com/3I9XOK2.png"></a></td>
    <td><a href="https://www.youtube.com/watch?v=blnhZC7OmMg" title="YouTube" rel="noopener"><img src="https://i.imgur.com/f9IgX6s.png"></a></td>
    <td><a href="https://www.youtube.com/watch?v=iRkz7FuJsA8" title="YouTube" rel="noopener"><img src="https://i.imgur.com/Vo5Zvmn.png"></a></td>
    <td><a href="https://www.youtube.com/watch?v=IHjEqAKDqjM" title="YouTube" rel="noopener"><img src="https://i.imgur.com/V9Zd81n.png"></a></td>
  </tr>
</table>

Hardware
------

At the moment openpilot supports the [EON Dashcam DevKit](https://comma.ai/shop/products/eon-dashcam-devkit). A [panda](https://shop.comma.ai/products/panda-obd-ii-dongle) and a [giraffe](https://comma.ai/shop/products/giraffe/) are recommended tools to interface the EON with the car. We'd like to support other platforms as well.

Install openpilot on a neo device by entering ``https://openpilot.comma.ai`` during NEOS setup.

Supported Cars
------

| Make                 | Model                    | Supported Package    | Lateral | Longitudinal   | No Accel Below   | No Steer Below | Giraffe           |
| ---------------------| -------------------------| ---------------------| --------| ---------------| -----------------| ---------------|-------------------|
| Acura                | ILX 2016-17              | AcuraWatch Plus      | Yes     | Yes            | 25mph<sup>1</sup>| 25mph          | Nidec             |
| Acura                | RDX 2018                 | AcuraWatch Plus      | Yes     | Yes            | 25mph<sup>1</sup>| 12mph          | Nidec             |
| Buick<sup>3</sup>    | Regal 2018               | Adaptive Cruise      | Yes     | Yes            | 0mph             | 7mph           | Custom<sup>7</sup>|
| Chevrolet<sup>3</sup>| Malibu 2017              | Adaptive Cruise      | Yes     | Yes            | 0mph             | 7mph           | Custom<sup>7</sup>|
| Chevrolet<sup>3</sup>| Volt 2017-18             | Adaptive Cruise      | Yes     | Yes            | 0mph             | 7mph           | Custom<sup>7</sup>|
| Cadillac<sup>3</sup> | ATS 2018                 | Adaptive Cruise      | Yes     | Yes            | 0mph             | 7mph           | Custom<sup>7</sup>|
| Chrysler             | Pacifica 2018            | Adaptive Cruise      | Yes     | Stock          | 0mph             | 9mph           | FCA               |
| Chrysler             | Pacifica Hybrid 2017-18  | Adaptive Cruise      | Yes     | Stock          | 0mph             | 9mph           | FCA               |
| Chrysler             | Pacifica Hybrid 2019     | Adaptive Cruise      | Yes     | Stock          | 0mph             | 39mph          | FCA               |
| GMC<sup>3</sup>      | Acadia Denali 2018       | Adaptive Cruise      | Yes     | Yes            | 0mph             | 7mph           | Custom<sup>7</sup>|
| Holden<sup>3</sup>   | Astra 2017               | Adaptive Cruise      | Yes     | Yes            | 0mph             | 7mph           | Custom<sup>7</sup>|
| Honda                | Accord 2018              | All                  | Yes     | Stock          | 0mph             | 3mph           | Bosch             |
| Honda                | Civic Sedan/Coupe 2016-18| Honda Sensing        | Yes     | Yes            | 0mph             | 12mph          | Nidec             |
| Honda                | Civic Sedan/Coupe 2019   | Honda Sensing        | Yes     | Stock          | 0mph             | 2mph           | Bosch             |
| Honda                | Civic Hatchback 2017-19  | Honda Sensing        | Yes     | Stock          | 0mph             | 12mph          | Bosch             |
| Honda                | CR-V 2015-16             | Touring              | Yes     | Yes            | 25mph<sup>1</sup>| 12mph          | Nidec             |
| Honda                | CR-V 2017-18             | Honda Sensing        | Yes     | Stock          | 0mph             | 12mph          | Bosch             |
| Honda                | CR-V Hybrid 2019         | All                  | Yes     | Stock          | 0mph             | 12mph          | Bosch             |
| Honda                | Odyssey 2017-19          | Honda Sensing        | Yes     | Yes            | 25mph<sup>1</sup>| 0mph           | Inverted Nidec    |
| Honda                | Passport 2019            | All                  | Yes     | Yes            | 25mph<sup>1</sup>| 12mph          | Inverted Nidec    |
| Honda                | Pilot 2016-18            | Honda Sensing        | Yes     | Yes            | 25mph<sup>1</sup>| 12mph          | Nidec             |
| Honda                | Pilot 2019               | All                  | Yes     | Yes            | 25mph<sup>1</sup>| 12mph          | Inverted Nidec    |
| Honda                | Ridgeline 2017-19        | Honda Sensing        | Yes     | Yes            | 25mph<sup>1</sup>| 12mph          | Nidec             |
| Hyundai              | Santa Fe 2019            | All                  | Yes     | Stock          | 0mph             | 0mph           | Custom<sup>6</sup>|
| Hyundai              | Elantra 2017             | SCC + LKAS           | Yes     | Stock          | 19mph            | 34mph          | Custom<sup>6</sup>|
| Hyundai              | Genesis 2018             | All                  | Yes     | Stock          | 19mph            | 34mph          | Custom<sup>6</sup>|
| Jeep                 | Grand Cherokee 2017-18   | Adaptive Cruise      | Yes     | Stock          | 0mph             | 9mph           | FCA               |
| Jeep                 | Grand Cherokee 2019      | Adaptive Cruise      | Yes     | Stock          | 0mph             | 39mph          | FCA               |
| Kia                  | Optima 2019              | SCC + LKAS           | Yes     | Stock          | 0mph             | 0mph           | Custom<sup>6</sup>|
| Kia                  | Sorento 2018             | All                  | Yes     | Stock          | 0mph             | 0mph           | Custom<sup>6</sup>|
| Kia                  | Stinger 2018             | SCC + LKAS           | Yes     | Stock          | 0mph             | 0mph           | Custom<sup>6</sup>|
| Lexus                | RX Hybrid 2016-19        | All                  | Yes     | Yes<sup>2</sup>| 0mph             | 0mph           | Toyota            |
| Subaru               | Crosstrek 2018           | EyeSight             | Yes     | Stock          | 0mph             | 0mph           | Subaru            |
| Subaru               | Impreza 2019             | EyeSight             | Yes     | Stock          | 0mph             | 0mph           | Subaru            |
| Toyota               | Avalon 2016              | TSS-P                | Yes     | Yes<sup>2</sup>| 20mph<sup>1</sup>| 0mph           | Toyota            |
| Toyota               | Camry 2018<sup>4</sup>   | All                  | Yes     | Stock          | 0mph<sup>5</sup> | 0mph           | Toyota            |
| Toyota               | C-HR 2017-18<sup>4</sup> | All                  | Yes     | Stock          | 0mph             | 0mph           | Toyota            |
| Toyota               | Corolla 2017-18          | All                  | Yes     | Yes<sup>2</sup>| 20mph<sup>1</sup>| 0mph           | Toyota            |
| Toyota               | Corolla Hatchback 2019   | All                  | Yes     | Yes            | 0mph             | 0mph           | Toyota            |
| Toyota               | Highlander 2017-18       | All                  | Yes     | Yes<sup>2</sup>| 0mph             | 0mph           | Toyota            |
| Toyota               | Highlander Hybrid 2018   | All                  | Yes     | Yes<sup>2</sup>| 0mph             | 0mph           | Toyota            |
| Toyota               | Prius 2016               | TSS-P                | Yes     | Yes<sup>2</sup>| 0mph             | 0mph           | Toyota            |
| Toyota               | Prius 2017-19            | All                  | Yes     | Yes<sup>2</sup>| 0mph             | 0mph           | Toyota            |
| Toyota               | Prius Prime 2017-19      | All                  | Yes     | Yes<sup>2</sup>| 0mph             | 0mph           | Toyota            |
| Toyota               | Rav4 2016                | TSS-P                | Yes     | Yes<sup>2</sup>| 20mph<sup>1</sup>| 0mph           | Toyota            |
| Toyota               | Rav4 2017-18             | All                  | Yes     | Yes<sup>2</sup>| 20mph<sup>1</sup>| 0mph           | Toyota            |
| Toyota               | Rav4 2019                | All                  | Yes     | Yes            | 0mph             | 0mph           | Toyota            |
| Toyota               | Rav4 Hybrid 2017-18      | All                  | Yes     | Yes<sup>2</sup>| 0mph             | 0mph           | Toyota            |

<sup>1</sup>[Comma Pedal](https://community.comma.ai/wiki/index.php/Comma_Pedal) is used to provide stop-and-go capability to some of the openpilot-supported cars that don't currently support stop-and-go. Here is how to [build a Comma Pedal](https://medium.com/@jfrux/comma-pedal-building-with-macrofab-6328bea791e8). ***NOTE: The Comma Pedal is not officially supported by [comma.ai](https://comma.ai)***  
<sup>2</sup>When disconnecting the Driver Support Unit (DSU), otherwise longitudinal control is stock ACC. For DSU locations, see [Toyota Wiki page](https://community.comma.ai/wiki/index.php/Toyota)  
<sup>3</sup>[GM installation guide](https://zoneos.com/volt/).  
<sup>4</sup>It needs an extra 120Ohm resistor ([pic1](https://i.imgur.com/CmdKtTP.jpg), [pic2](https://i.imgur.com/s2etUo6.jpg)) on bus 3 and giraffe switches set to 01X1 (11X1 for stock LKAS), where X depends on if you have the [comma power](https://comma.ai/shop/products/power/).  
<sup>5</sup>28mph for Camry 4CYL L, 4CYL LE and 4CYL SE which don't have Full-Speed Range Dynamic Radar Cruise Control.  
<sup>6</sup>Open sourced [Hyundai Giraffe](https://github.com/commaai/neo/tree/master/giraffe/hyundai) is designed for the 2019 Sante Fe; pinout may differ for other Hyundais.  
<sup>7</sup>Community built Giraffe, find more information [here](https://zoneos.com/shop/).  

Community Maintained Cars
------

The port was started by Andrew Frahn of Emmertex.  
@ku7 on commaai Slack, and ku7 tech on youtube
https://www.youtube.com/c/ku7tech
Please support the port, and if you can, please help support me!



What is special about this port?
------

It's unfettered awesome with no corporate fears!
Where non standard features were made by someone other than me @ku7, they are credited with there Slack Username

Based on OpenPilot 0.5.9 from comma.ai

- Auto-Port almost all Hyundai/Kia/Genesis
- Do not disable when Accelerator is depressed (MAD button*)
- Disable auto-steering on blinker, but leave OP engaged
- - Disabled on first blink, and stays disabled until 1 second of no blinking.
- Sounds! (Thanks Sid and @BogGyver and #Tesla in general) (SND button*)
- Tesla UI (Thanks everyone in #Tesla)
- - 3 Switch positions change the display, you probably want it far left.*
- Advanced Lane Change Assist (Thanks @BogGyver) (ALCA button*)*
- - And with Blind Spot Detection for any Kia/Hyundai with it
- Panda auto-detects Camera Pinout
- - And now so does OP!  LKAS on CAN 2 or CAN 3, it doesn't matter!
- No need for giraffe switches, If no EON, then forwards stock camera (Thanks @JamesT-1)
- Dashcam Recorder (Thanks @pjlao307)
- Full Time Stock LKAS passthrough*
- - Including High Beam Assist and Automatic Emergency Braking, Blind Spot, Traffic Sign Detection, and more.
- - This includes Land Departure Warning, but stock LKAS must be enabled for this.
- Optional Dynamic Stock and OP Steering.  The moment OP isn't steering, it switched back to Stock (LKAS button*)*
- ** Temporarily removed ** CLI Based Real Time Tuning (Thanks @JamesT-1)
- Unsupported cars default to A special 'unsupported car'.  This should work for most cars.
- Cruise Setpoint set from OSM Speed Limit*
- Compress when not uploading
- Automatically detects CAN Specifics (checksum, SCC, so on)
- New Lateral Control from @Gernby
- Probably other things I have forgotten

* Has known issues

Known issues
If your car has adaptive cruise control and lane keep assist, you are in luck. Using a [panda](https://comma.ai/shop/products/panda-obd-ii-dongle/) and [cabana](https://community.comma.ai/cabana/), you can understand how to make your car drive by wire.

We've written guides for [Brand](https://medium.com/@comma_ai/how-to-write-a-car-port-for-openpilot-7ce0785eda84) and [Model](https://medium.com/@comma_ai/openpilot-port-guide-for-toyota-models-e5467f4b5fe6) ports. These guides might help you after you have the basics figured out.

- BMW, Audi, Volvo, and Mercedes all use [FlexRay](https://en.wikipedia.org/wiki/FlexRay) and can be supported after [FlexRay support](https://github.com/commaai/openpilot/pull/463) is merged.
- We put time into a Ford port, but the steering has a 10 second cutout limitation that makes it unusable.
- The 2016-2017 Honda Accord uses a custom signaling protocol for steering that's unlikely to ever be upstreamed.

Directory structure
------
    .
    ├── apk                 # The apk files used for the UI
    ├── cereal              # The messaging spec used for all logs on EON
    ├── common              # Library like functionality we've developed here
    ├── installer/updater   # Manages auto-updates of openpilot
    ├── opendbc             # Files showing how to interpret data from cars
    ├── panda               # Code used to communicate on CAN and LIN
    ├── phonelibs           # Libraries used on EON
    ├── pyextra             # Libraries used on EON
    └── selfdrive           # Code needed to drive the car
        ├── assets          # Fonts and images for UI
        ├── athena          # Allows communication with the app
        ├── boardd          # Daemon to talk to the board
        ├── can             # Helpers for parsing CAN messages
        ├── car             # Car specific code to read states and control actuators
        ├── common          # Shared C/C++ code for the daemons
        ├── controls        # Perception, planning and controls
        ├── debug           # Tools to help you debug and do car ports
        ├── locationd       # Soon to be home of precise location
        ├── logcatd         # Android logcat as a service
        ├── loggerd         # Logger and uploader of car data
        ├── mapd            # Fetches map data and computes next global path
        ├── proclogd        # Logs information from proc
        ├── sensord         # IMU / GPS interface code
        ├── test            # Car simulator running code through virtual maneuvers
        ├── ui              # The UI
        └── visiond         # Vision pipeline

To understand how the services interact, see `selfdrive/service_list.yaml`

User Data / chffr Account / Crash Reporting
------

- ALCA (Advanced Lane Change Assist) is not properly tuned.  Use with caution
- CAM (Stock LKAS Forwarding) occasionally silenetly faults, turning off stock LKAS
- Auto Speed Setpoint Control is irregular, the button spamming works perfect some times, not at all others
- Tri-State Switch is currently broken in NEOS, NEOS fix is needed
- Touch Events don't work properly in the new NEOS, changes are needed
- Panda Safety doesn't really exist

Contributing
------

We welcome both pull requests and issues on [github](http://github.com/commaai/openpilot). Bug fixes and new car ports encouraged.

We also have a [bounty program](https://comma.ai/bounties.html).

Want to get paid to work on openpilot? [comma.ai is hiring](https://comma.ai/jobs/)

Licensing
------

openpilot is released under the MIT license. Some parts of the software are released under other licenses as specified.

Any user of this software shall indemnify and hold harmless Comma.ai, Inc. and its directors, officers, employees, agents, stockholders, affiliates, subcontractors and customers from and against all allegations, claims, actions, suits, demands, damages, liabilities, obligations, losses, settlements, judgments, costs and expenses (including without limitation attorneys’ fees and costs) which arise out of, relate to or result from any use of this software by user.

**THIS IS ALPHA QUALITY SOFTWARE FOR RESEARCH PURPOSES ONLY. THIS IS NOT A PRODUCT.
YOU ARE RESPONSIBLE FOR COMPLYING WITH LOCAL LAWS AND REGULATIONS.
NO WARRANTY EXPRESSED OR IMPLIED.**

---

<img src="https://d1qb2nb5cznatu.cloudfront.net/startups/i/1061157-bc7e9bf3b246ece7322e6ffe653f6af8-medium_jpg.jpg?buster=1458363130" width="75"></img> <img src="https://cdn-images-1.medium.com/max/1600/1*C87EjxGeMPrkTuVRVWVg4w.png" width="225"></img>
