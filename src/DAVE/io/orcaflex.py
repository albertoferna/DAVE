"""
DAVE to ORCAFLEX yaml

This is an incomplete export from DAVE to Orcaflex.

We are using the yaml format instead of the orcaflex API because writing to yaml does not require an orcaflex license.

Supported are:

- Rigid bodies without parent --> 6D buoys
- Rigid bodies with a parent and fully fixed -->  6D buoy
- Rigid body or axis partially fixed:
     --> use constraint
- Cables --> winches

"""

from DAVE import *

def write_ofx_run_and_collect_script(py_file, yml_file, ofx_path=None):
    """Creates a .py file which will run the given orcaflex model (yml_file) and extract its data after solving statics.
    The results will be saved to a file with the same name as the model .yml file but with _sum appended to the file-name.

    so running
    model.yml

    will create
    model_sum.yml

    """

    _ofx_run_collect_py = """
# Import the orcaflex api
import sys
$PATH$ # sys.path.append(r'...\OrcFxAPI\Python')
import OrcFxAPI as ofx

import yaml

# Load the model
print('Loading')

$LOAD$ # ofx_file = r'c:\data\ofx.yml'
m = ofx.Model(ofx_file)

print('Calculating statics')
m.CalculateStatics()

p6DBuoy_static = ['X','Y','Z',
                  'Rotation 1','Rotation 2','Rotation 3']
pWinch_static = ['Tension','Stretched Length']

nodes = {}

for obj in m.objects:
    # print(obj.name)
    
    if obj.type == ofx.ot6DBuoy:
        props = p6DBuoy_static
    elif obj.type == ofx.otWinch:
        props = pWinch_static
    else:
        continue

    results = {}
        
    for p in props:
        value = obj.StaticResult(p)
        results[p] = float(value)

    nodes[obj.name] = results


s = yaml.dump(nodes, explicit_start=True)

$FILENAME$ # filename = f'c:\data\ofx_results.yml'

with open(filename,'w') as f:
    f.write(s)
    
print(f'Done writing {filename}')
    """

    contents = _ofx_run_collect_py
    if ofx_path is None:
        contents = contents.replace('$PATH$', '')
    else:
        contents = contents.replace('$PATH$', f'sys.path.append(r"{ofx_path}")')

    outfile = str(yml_file)[:-4] + '_sum.yml'

    contents = contents.replace('$FILENAME$',f'filename = r"{outfile}"')
    contents = contents.replace('$LOAD$',f'ofx_file = r"{yml_file}"')

    with open(py_file, 'w') as f:
        f.write(contents)

    print(f'Written {py_file} to run {yml_file} and save resuts as {outfile}')



import yaml
from scipy.spatial.transform import Rotation

OFX_ZERO_MASS = 1e-6
RHO = 1.025
G = 9.81


def rotation_to_attitude(rotation):
    """Converts a rotation vector to orcaflex attitudes (rotation 1,2,3) [deg]"""
    r = Rotation.from_rotvec(np.deg2rad(rotation))
    eu = r.as_euler(seq='zyx',degrees=True).tolist()
    return [eu[2], eu[1], eu[0]]

def attitude_to_rotvec(rot123):
    """Converts an orcaflex attitude (rotation1 rotation2 rotation3) to a rotation vector [deg]"""
    rx, ry, rz = rot123
    r = Rotation.from_euler(angles = (rz,ry,rx), seq='zyx', degrees=True)
    return np.degrees(r.as_rotvec())

def export_ofx_yml(s, filename):
    """Convert the scene to a orcaflex .yml file. Only compatible nodes are exported. Make the scene  orcaflex compatible before exporting

    Args:
        s : Scene
        filename : file to write to (.yml)
    """

    s.sort_nodes_by_dependency()

    buoys = []
    winches = []
    constraints = []
    vessel_types = []
    vessels = []
    Shapes = []

    for n in s._nodes:

        if isinstance(n, (RigidBody, Axis)):

            if isinstance(n, RigidBody):
                mass = max(n.mass, OFX_ZERO_MASS)
                I = (mass * n.inertia_radii ** 2).tolist()
                cog = [*n.cog]

            else:
                mass = OFX_ZERO_MASS
                I = [OFX_ZERO_MASS, OFX_ZERO_MASS, OFX_ZERO_MASS]
                cog = [0, 0, 0]

            # check the connection

            pos = [*n.position]
            rot = [*rotation_to_attitude(n.rotation)]

            if not any(n.fixed):
                connection = 'Free'

            elif np.all(n.fixed):
                if n.parent is None:
                    connection = 'Fixed'
                else:
                    connection = n.parent.name

            else:
                # Partially fixed - create constraint

                cname = n.name + ' [fixes]'

                if n.parent is None:
                    connection = 'Fixed'
                else:
                    connection = n.parent.name

                fixes = []
                for f in n.fixed:
                    if f:
                        fixes.append('No')
                    else:
                        fixes.append('Yes')

                c = {'Name': cname,
                     'Connection': connection,
                     'DOFFree': fixes,
                     'InitialPosition': pos,
                     'InitialAttitude': rot,
                     }

                constraints.append(c)

                # set the props for the 6d buoy
                connection = cname
                pos = [0,0,0]
                rot = [0,0,0]

            b = {'Name': n.name,
                 'Connection': connection,
                 'InitialPosition': pos,
                 'InitialAttitude': rot,
                 'Mass': mass,
                 'Volume': 0,
                 'MomentsOfInertia': I,
                 'CentreOfMass': cog
                 }                       # create the basic buoy, but do not add it yet as some of the properties may be
                                         # overwritten by the vessel that we may create now

            ## Vessels --------------
            #
            # If one of the children of this Axis is a HydSpring (linear hydrostatics node), then
            #  1. Look for a waveinteraction1 node as well
            #
            # if both are found then
            # 1. create a vessel type
            # 2. create a vessel without any mass
            # 3. place the buoy that we just created on the vessel

            children = s.nodes_with_parent(n)

            hyd_spring = None
            hyd_db = None

            for child in children:
                cn = s[child]
                if isinstance(cn, HydSpring):
                    hyd_spring = cn
                if isinstance(cn, WaveInteraction1):
                    hyd_db = cn

            if hyd_spring is not None:
                # create a vessel type

                vt = {'Name': n.name + hyd_spring.name,
                      'Length':1,
                      # conventions
                      'WavesReferredToBy':'frequency (rad/s)',
                      'RAOPhaseConvention':'leads',
                      'RAOPhaseUnitsConvention':'radians'
                      }

                # Stiffness, Added mass, damping
                #
                # The Reference-origin defines where all of these forces are applied
                # so it needs to be the origin of the hydrodynamic data, if we have any

                ref_origin = (0.,0.,0.)
                if hyd_db is not None:
                    ref_origin = hyd_db.offset

                # calculate the stiffness matrix relative to this point

                k = np.zeros((3,3))

                # Heave and heave coupling
                k[0,0] = hyd_spring.kHeave
                k[0,1] = -hyd_spring.kHeave * (hyd_spring.cob[1] + hyd_spring.COFY - ref_origin[1]) # heave-roll
                k[0,2] = -hyd_spring.kHeave * (hyd_spring.cob[0] + hyd_spring.COFX - ref_origin[0])  # heave-pitch
                k[1,0] = k[0,1]
                k[2,0] = k[0,2]

                # BML and BMT
                k[1,1] = hyd_spring.displacement_kN * hyd_spring.BMT # g * rho * disp * BMt
                k[2, 2] = hyd_spring.displacement_kN * hyd_spring.BML  # g * rho * disp * BMt

                d = {'Name':'Draught1',
                     'Mass':1e-6,
                     'MomentOfInertiaTensorX': [0.001,0,0],
                     'MomentOfInertiaTensorY': [0,0.001,0],
                     'MomentOfInertiaTensorZ': [0,0,0.001],
                     'CentreOfGravityX': 0,
                     'CentreOfGravityY': 0,
                     'CentreOfGravityZ': 0,
                     'CentreOfBuoyancyX' : hyd_spring.cob[0],
                     'CentreOfBuoyancyY' : hyd_spring.cob[1],
                     'CentreOfBuoyancyZ' : hyd_spring.cob[2],

                     # Stiffness, added mass, damping
                     'StiffnessInertiaDampingRefOriginx':ref_origin[0],
                     'StiffnessInertiaDampingRefOriginy':ref_origin[1],
                     'StiffnessInertiaDampingRefOriginz':ref_origin[2],
                     'HydrostaticReferenceOriginDatumPositionz':n.to_glob_position(ref_origin)[2],
                     'HydrostaticReferenceOriginDatumOrientationx':0,
                     'HydrostaticReferenceOriginDatumOrientationy':0,
                     'DisplacedVolume': hyd_spring.displacement_kN / (RHO * G),
                     'HydrostaticStiffnessz' : k[:,0].tolist(),
                     'HydrostaticStiffnessRx':k[:,1].tolist(),
                     'HydrostaticStiffnessRy': k[:,2].tolist(),

                     # other damping settings

                     # 'OtherDampingCalculatedFrom',  # Add once version > 10.2d

                     'OtherDampingOriginx':ref_origin[0],
                     'OtherDampingOriginy':ref_origin[1],
                     'OtherDampingOriginz':ref_origin[2],
                     'OtherDampingLinearCoeffx':0,
                     'OtherDampingLinearCoeffy':0,
                     'OtherDampingLinearCoeffz':0,
                     'OtherDampingLinearCoeffRx':0,
                     'OtherDampingLinearCoeffRy':0,
                     'OtherDampingLinearCoeffRz':0,
                     'OtherDampingQuadraticCoeffx':0,
                     'OtherDampingQuadraticCoeffy':0,
                     'OtherDampingQuadraticCoeffz':0,
                     'OtherDampingQuadraticCoeffRx':0,
                     'OtherDampingQuadraticCoeffRy':0,
                     'OtherDampingQuadraticCoeffRz':0

                     }

                # Export hydrodynamics, if any
                if hyd_db is not None:

                    # Export
                    # Wave-forces (Force RAOs)
                    # Damping
                    # Added mass

                    LoadRAOs = {'RAOOriginX': ref_origin[0],  # TODO: These values do not seem to be loaded into OFX
                            'RAOOriginY': ref_origin[1],
                            'RAOOriginZ': ref_origin[2]}

                    # load the database
                    from mafredo.hyddb1 import Hyddb1
                    database = s.get_resource_path(hyd_db.path)
                    db = Hyddb1()
                    db.load_from(database)

                    # get the available headings
                    a_headings = db.force_rao(0)._data['wave_direction'].values
                    a_frequencies = db.frequencies

                    rao_mode = []
                    for i in range(6):
                        rao_mode.append(db.force_rao(i))

                    RAOs = []

                    for heading in a_headings:

                        rao = {'RAODirection':float(heading)}

                        RAOPeriodOrFrequency = []
                        RAOSurgeAmp = []
                        RAOSurgePhase = []
                        RAOSwayAmp = []
                        RAOSwayPhase = []
                        RAOHeaveAmp = []
                        RAOHeavePhase = []
                        RAORollAmp = []
                        RAORollPhase = []
                        RAOPitchAmp = []
                        RAOPitchPhase = []
                        RAOYawAmp = []
                        RAOYawPhase = []

                        for frequency in a_frequencies:
                            RAOPeriodOrFrequency.append(float(frequency))

                            r = rao_mode[0].get_value(wave_direction=heading, omega = frequency)
                            RAOSurgeAmp.append(float(np.abs(r)))
                            RAOSurgePhase.append(float(np.angle(r)))

                            r = rao_mode[1].get_value(wave_direction=heading, omega=frequency)
                            RAOSwayAmp.append(float(np.abs(r)))
                            RAOSwayPhase.append(float(np.angle(r)))

                            r = rao_mode[2].get_value(wave_direction=heading, omega=frequency)
                            RAOHeaveAmp.append(float(np.abs(r)))
                            RAOHeavePhase.append(float(np.angle(r)))

                            r = rao_mode[3].get_value(wave_direction=heading, omega=frequency)
                            RAORollAmp.append(float(np.abs(r)))
                            RAORollPhase.append(float(np.angle(r)))

                            r = rao_mode[4].get_value(wave_direction=heading, omega=frequency)
                            RAOPitchAmp.append(float(np.abs(r)))
                            RAOPitchPhase.append(float(np.angle(r)))

                            r = rao_mode[5].get_value(wave_direction=heading, omega=frequency)
                            RAOYawAmp.append(float(np.abs(r)))
                            RAOYawPhase.append(float(np.angle(r)))

                        rao['RAOPeriodOrFrequency'] = RAOPeriodOrFrequency
                        rao['RAOSurgeAmp'] = RAOSurgeAmp
                        rao['RAOSurgePhase'] = RAOSurgePhase
                        rao['RAOSwayAmp'] = RAOSwayAmp
                        rao['RAOSwayPhase'] = RAOSwayPhase
                        rao['RAOHeaveAmp'] = RAOHeaveAmp
                        rao['RAOHeavePhase'] = RAOHeavePhase
                        rao['RAORollAmp'] = RAORollAmp
                        rao['RAORollPhase'] = RAORollPhase
                        rao['RAOPitchAmp'] = RAOPitchAmp
                        rao['RAOPitchPhase'] = RAOPitchPhase
                        rao['RAOYawAmp'] = RAOYawAmp
                        rao['RAOYawPhase'] = RAOYawPhase
                        RAOs.append(rao)

                    LoadRAOs['RAOs'] = RAOs
                    d['LoadRAOs'] = LoadRAOs

                    # Added mass and Damping
                    FrequencyDependentAddedMassAndDamping = []
                    for frequency in a_frequencies:
                        entry = {'AMDPeriodOrFrequency': float(frequency)}
                        B = db.damping(frequency)
                        A = db.amass(frequency)

                        # Make symmetric (else Orcaflex will not read the yml)

                        def make_orcaflex_happy(mat):
                            mat = 0.5 * mat + 0.5 * mat.transpose()
                            R = np.zeros((6, 6))
                            R[0, 0] = mat[0, 0]
                            R[1, 1] = mat[1, 1]
                            R[2, 2] = mat[2, 2]
                            R[3, 3] = mat[3, 3]
                            R[4, 4] = mat[4, 4]
                            R[5, 5] = mat[5, 5]

                            # oA[0,2] = 7   # error
                            R[2, 0] = mat[2, 0]

                            R[0, 4] = mat[0, 4]
                            R[4, 0] = mat[0, 4]

                            R[1, 3] = mat[1, 3]  # need both
                            R[3, 1] = mat[1, 3]

                            R[1, 5] = mat[1, 5]  # need both
                            R[5, 1] = mat[1, 5]

                            R[5, 3] = mat[3, 5]
                            return R

                        oA = make_orcaflex_happy(A)
                        oB = make_orcaflex_happy(B)

                        entry['AddedMassMatrixX'] = oA[0].tolist()
                        entry['AddedMassMatrixY'] = oA[1].tolist()
                        entry['AddedMassMatrixZ'] = oA[2].tolist()
                        entry['AddedMassMatrixRx'] = oA[3].tolist()
                        entry['AddedMassMatrixRy'] = oA[4].tolist()
                        entry['AddedMassMatrixRz'] = oA[5].tolist()

                        entry['DampingX'] = oB[0].tolist()
                        entry['DampingY'] = oB[1].tolist()
                        entry['DampingZ'] = oB[2].tolist()
                        entry['DampingRx'] = oB[3].tolist()
                        entry['DampingRy'] = oB[4].tolist()
                        entry['DampingRz'] = oB[5].tolist()

                        FrequencyDependentAddedMassAndDamping.append(entry)

                    d['AMDMethod'] = 'Frequency Dependent'
                    d['FrequencyDependentAddedMassAndDamping'] = FrequencyDependentAddedMassAndDamping

                vt['Draughts'] = [d]  # draughts is a list! Even though we only use one.

                # Create a vessel

                v = {'Name':n.name + 'Vessel',
                     'VesselType':n.name + hyd_spring.name,
                     'Length':1,
                     'InitialPosition': pos,
                     'InitialHeel': float(n.heel),
                     'InitialTrim': float(n.trim),
                     'InitialHeading': float(n.heading),
                     'IncludedInStatics': '6 DOF',
                     'PrimaryMotion': 'Calculated (6 DOF)',
                     'SuperimposedMotion': 'None',
                     'PrimaryMotionIsTreatedAs': 'Wave frequency',
                     'IncludeWaveLoad1stOrder': 'Yes',
                     'IncludeAddedMassAndDamping': 'Yes',
                     'IncludeOtherDamping': 'Yes'}

                # Modify the buoy to be on the vessel
                b['InitialPosition'] = [0,0,0]
                b['InitialAttitude'] = [0,0,0]
                b['Connection'] = v['Name']

                vessel_types.append(vt)
                vessels.append(v)




            # Done with the vessel stuff, back to the 6D buoy that we were exporting


            buoys.append(b)




        if isinstance(n, Cable):

            connection = []
            connectionX = []
            connectionY = []
            connectionZ = []

            for c in n.connections:
                # either a point or a circle
                # for now only points are supported

                if isinstance(c, Circle):
                    raise ValueError('Circles not yet supported')

                if c.parent is None:
                    connection.append('Fixed')
                else:
                    connection.append(c.parent.name)
                connectionX.append(c.position[0])
                connectionY.append(c.position[1])
                connectionZ.append(c.position[2])

            w = { 'Name': n.name,
                  'Connection': connection,
                  'ConnectionX': connectionX,
                  'ConnectionY': connectionY,
                  'ConnectionZ': connectionZ,
                  'Stiffness': n.EA,
                  'NumberOfConnections': len(n.connections),
                  'WinchControlType': 'By Stage',
                  'StageMode': ['Specified Length','Specified Payout','Specified Payout'],
                  'StageValue': [n.length,0,0]
                  }

            winches.append(w)

        if isinstance(n, Visual):

            shape = { 'Name': n.name,
                  'Connection':n.parent.name,
                  'ShapeType':'Drawing',
                  'Shape' : 'Block',
                  'OriginX' : 0 ,
                  'OriginY' : 0 ,
                  'OriginZ' : 0 ,
                  'Rotation1' : 0 ,
                  'Rotation2' : 0 ,
                  'Rotation3' : 0 ,
                  'ShadedDrawingFileName' : str(s.get_resource_path(n.path)) ,
                  'ShadedDrawingMirrorInPlane' : 'XZ plane' ,
                  'ShadedDrawingRotation1' : 0 ,
                  'ShadedDrawingRotation2' : 90 ,
                  'ShadedDrawingRotation3' : -90 }

            Shapes.append(shape)


    # Write the yml

    data = dict()

    if buoys:
        data['6DBuoys'] = buoys
    if winches:
        data['Winches'] = winches
    if constraints:
        data['Constraints'] = constraints
    if vessel_types:
        data['VesselTypes'] = vessel_types
    if vessels:
        data['Vessels'] = vessels
    if Shapes:
        data['Shapes'] = Shapes

    s = yaml.dump(data, explicit_start=True)

    with open(filename,'w') as f:
        f.write(s)

def run_statics_collect(s, filename=None, try_rerun = True):
    """Obtains the orcaflex static resuls for the given scene. Runs orcaflex if possible and try_rerun is not False

    If OrcFxAPI can be imported and not try_rerun:
        creates a orcaflex model in .yml format
        opens orcaflex API
        loads .yml file
        solves statics
        collects the results
        saves them as a .yml file

    opens the summary file
    returns the results as a dict.
    """

    import os
    tempdir = os.environ['TEMP']

    if filename is None:
        # make a temporary file
        # we are going to run orcaflex, and orcaflex only works on windows,
        # so it is save to assume that we are on windows
        filename = tempdir + r'\ofx_temp_dave_file.yml'

        print(f'Using a temporary file here: {filename}')

    export_ofx_yml(s, filename)

    # create a run-file
    run_file = tempdir + r'\ofx_dave_runfile.py'

    write_ofx_run_and_collect_script(py_file=run_file, yml_file=filename)

    # run the file
    exec(open(run_file).read())

    # read the results
    outfile = str(filename)[:-4] + '_sum.yml'

    with open(outfile, 'r') as f:
        result = yaml.load(f, Loader=yaml.BaseLoader)

    return result











def compare_statics(s, ofx_sum):
    """Compares the static state of s to the static results of ofx_sum.

    Args:
        s : Scene
        ofx_sum : ofx summary dict or ofx_sum yml filename (str or Path)

    Returns:
        dict with results

    """

    if isinstance(ofx_sum,dict):
        pass
    else:
        with open(ofx_sum, 'r') as f:
            ofx_sum = yaml.load(f, Loader=yaml.BaseLoader)

    # do the comparison
    results = []

    for n in s._nodes:

        if isinstance(n, Axis):
            # Compare position and orientation

            d = ofx_sum[n.name]
            ofx_global_pos = (d['X'], d['Y'], d['Z'])
            ofx_rot123 = (d['Rotation 1'], d['Rotation 2'], d['Rotation 3'])
            ofx_rotvec = attitude_to_rotvec((ofx_rot123))

            results.append( {'Name': n.name,
                              'Prop': 'global position [m,m,m]',
                              'Orcaflex': ofx_global_pos,
                              'DAVE': n.global_position})

            results.append( {'Name': n.name,
                              'Prop': 'global rotation vec [deg,deg,deg]',
                              'Orcaflex': ofx_rotvec,
                              'DAVE': n.global_rotation})

        if isinstance(n, Cable):
            # Compare position and orientation

            d = ofx_sum[n.name]

            results.append({'Name': n.name,
                            'Prop': 'Tension [kN]',
                            'Orcaflex': d['Tension'],
                            'DAVE': n.tension})

            results.append({'Name': n.name,
                            'Prop': 'Stretched length [m]',
                            'Orcaflex': d['Stretched Length'],
                            'DAVE': n.stretch + n.length})

    return results


if __name__ == "__main__":
    s = Scene('barge with linear hydrostatics.dave')
    s.solve_statics()

    yml_filename = r"c:\data\barge.yml"
    export_ofx_yml(s, yml_filename)

    py_file = r"c:\data\run_barge.py"

    ofx_api_path = r'C:\Program Files (x86)\Orcina\OrcaFlex\10.2\OrcFxAPI\Python'

    write_ofx_run_and_collect_script(py_file=py_file, yml_file=yml_filename, ofx_path=ofx_api_path)

    results = compare_statics(s, r"I:\barge_sum.yml")

    import pandas as pd

    df = pd.DataFrame.from_dict(results)

    print(df)


