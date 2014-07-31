from nose.tools import *
import whetlab, whetlab_api
from time import time, sleep

default_access_token = None

default_description = ''
default_parameters = { 'p1':{'type':'float', 'min':0, 'max':10.0, 'size':1},
                            'p2':{'type':'integer', 'min':0, 'max':10, 'size':1}}
default_outcome = {'name':'Dummy outcome', 'type':'float'}

def test_required_prop_are_supported():
    """ All required properties should be supported, for parameters and outcome. """
    
    # Parameters
    for x in whetlab.required_properties:
        assert( x in whetlab.supported_properties )

    # Outcome
    for x in whetlab.outcome_required_properties:
        assert( x in whetlab.outcome_supported_properties )

def test_default_values_are_legal():
    """ All default values for properties should be legal, for parameters and outcome. """
    
    #Parameters
    for k,v in whetlab.default_values.items():
        if k in whetlab.legal_values:
            assert( v in whetlab.legal_values[k] )

    # Outcome
    for k,v in whetlab.outcome_default_values.items():
        if k in whetlab.outcome_legal_values:
            assert( v in whetlab.outcome_legal_values[k] )

def test_delete_experiment():
    """ Delete experiment should remove the experiment from the server. """
    
    name = 'test ' + str(time())
    scientist = whetlab.Experiment(access_token=default_access_token,
                                   name=name,
                                   description=default_description,
                                   parameters=default_parameters,
                                   outcome=default_outcome)
    
    scientist.update({'p1':5.,'p2':1},5)

    # Delete experiment
    whetlab.delete_experiment(default_access_token,name)

    # Should now be possible to create an experiment with the same name
    scientist = whetlab.Experiment(access_token=default_access_token,
                                   name=name,
                                   description=default_description,
                                   parameters=default_parameters,
                                   outcome=default_outcome)
    
    # Re-deleting it
    whetlab.delete_experiment(default_access_token,name)


class TestExperiment:

    @raises(whetlab_api.error.client_error.ClientError)
    def test_same_name(self):
        """ Can't create two experiments with same name (when resume is False). """

        name = 'test ' + str(time())
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=default_parameters,
                                       outcome=default_outcome)

        # Repeat Experiment creation to raise error, with resume set to False
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description+'2',
                                       parameters=default_parameters,
                                       outcome=default_outcome,
                                       resume = False)

        
    def test_resume_false(self):
        """ If resume is False and experiment's name is unique, can create an experiment. """

        name = 'test ' + str(time())
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=default_parameters,
                                       outcome=default_outcome,
                                       resume = False)
        
    def test_resume(self):
        """ Resume correctly loads previous results. """

        name = 'test ' + str(time())
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=default_parameters,
                                       outcome=default_outcome)

        scientist.update({'p1':2.1,'p2':1},3)

        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description)
        # Make sure result is still there
        assert( cmp(scientist._ids_to_param_values.values()[0],{'p1':2.1,'p2':1}) == 0 )
        assert( cmp(scientist._ids_to_outcome_values.values()[0],3) == 0 )

        whetlab.delete_experiment(default_access_token,name) 

    @raises(ValueError)
    def test_empty_name(self):
        """ Experiment's name can't be empty. """

        name = ''
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=default_parameters,
                                       outcome=default_outcome)

    @raises(whetlab_api.error.client_error.ClientError)
    def test_name_too_long(self):
        """ Experiment's name must have at most 500 caracters. """

        name = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=default_parameters,
                                       outcome=default_outcome)



#    @raises(whetlab_api.error.client_error.ClientError)
#    def test_description_too_long(self):
#        """ Experiment's description must have at most 500 caracters. """
#
#        name = 'test ' + str(time())
#        description = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
#        scientist = whetlab.Experiment(access_token=default_access_token,
#                                       name=name,
#                                       description=description,
#                                       parameters=default_parameters,
#                                       outcome=default_outcome)



    @raises(ValueError)
    def test_empty_parameters(self):
        """ Experiment's parameters can't be empty. """

        name = 'test ' + str(time())
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters={},
                                       outcome=default_outcome)

    @raises(ValueError)
    def test_empty_outcome(self):
        """ Experiment's outcome can't be empty. """

        name = 'test ' + str(time())
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=default_parameters,
                                       outcome={})

        whetlab.delete_experiment(default_access_token,name) 

    @raises(ValueError)
    def test_unknown_parameter_properties(self):
        """ Parameter properties must be valid. """

        name = 'test ' + str(time())
        bad_parameters = { 'p1':{'type':'float', 'min':0, 'max':10.0, 'size':1, 'fake_property':10}}
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=bad_parameters,
                                       outcome=default_outcome)

    @raises(ValueError)
    def test_min_max_properties(self):
        """ Parameter property 'min' must be smaller than 'max'. """

        name = 'test ' + str(time())
        bad_parameters = { 'p1':{'type':'float', 'min':10., 'max':1., 'size':1}}
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=bad_parameters,
                                       outcome=default_outcome)

    @raises(ValueError)
    def test_float_for_int_bounds(self):
        """ Parameter properties 'min' and 'max' must be integers if the parameter is an integer. """

        name = 'test ' + str(time())
        bad_parameters = { 'p1':{'type':'integer', 'min':0.0, 'max':0.5, 'size':1}}
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=bad_parameters,
                                       outcome=default_outcome)

    @raises(ValueError)
    def test_legal_property_value(self):
        """ Parameter property must take a legal value. """

        name = 'test ' + str(time())
        bad_parameters = { 'p1':{'type':'BAD_VALUE', 'min':1., 'max':10., 'size':1}}
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=bad_parameters,
                                       outcome=default_outcome)

    @raises(ValueError)
    def test_enum_not_supported(self):
        """ Parameter type 'enum' not yet supported. """

        name = 'test ' + str(time())
        bad_parameters = { 'p1':{'type':'enum', 'min':1., 'max':10., 'size':1}}
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=bad_parameters,
                                       outcome=default_outcome)

    @raises(whetlab_api.error.client_error.ClientError)
    def test_access_token(self):
        """ Valid access token must be provided. """

        name = 'test ' + str(time())
        scientist = whetlab.Experiment(access_token='',
                                       name=name,
                                       description=default_description,
                                       parameters=default_parameters,
                                       outcome=default_outcome)

    def test_cancel(self):
        """ Cancel removes a result. """

        name = 'test ' + str(time())
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=default_parameters,
                                       outcome=default_outcome)

        scientist.update({'p1':5.1,'p2':5},10)
        scientist.cancel({'p1':5.1,'p2':5})
        
        # Make sure result was removed
        scientist._sync_with_server()
        assert( len(scientist._ids_to_param_values) == 0 )
        assert( len(scientist._ids_to_outcome_values) == 0 )
        
        whetlab.delete_experiment(default_access_token,name) 

    def test_update(self):
        """ Update adds and can overwrite a result. """

        name = 'test ' + str(time())
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=default_parameters,
                                       outcome=default_outcome)

        scientist.update({'p1':5.1,'p2':5},10)

        # Make sure result was added
        scientist._sync_with_server()
        assert( cmp(scientist._ids_to_param_values.values()[0],{'p1':5.1,'p2':5}) == 0 )
        assert( cmp(scientist._ids_to_outcome_values.values()[0],10) == 0 )

        # Make sure result was overwritten
        scientist.update({'p1':5.1,'p2':5},20)
        scientist._sync_with_server()
        assert( len(scientist._ids_to_param_values.values()) == 1 )
        assert( len(scientist._ids_to_outcome_values.values()) == 1 )
        assert( cmp(scientist._ids_to_param_values.values()[0],{'p1':5.1,'p2':5}) == 0 )
        assert( cmp(scientist._ids_to_outcome_values.values()[0],20) == 0 )

        whetlab.delete_experiment(default_access_token,name) 

    def test_update_none(self):
        """ Update with a None outcome works and adds to pending results. """

        name = 'test ' + str(time())
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=default_parameters,
                                       outcome=default_outcome)

        scientist.update({'p1':5.1,'p2':5},None)

        # Make sure result was added to pending
        assert( len(scientist.pending()) == 1 )
        assert( cmp(scientist.pending()[0],{'p1':5.1,'p2':5}) == 0 )


        whetlab.delete_experiment(default_access_token,name) 

    def test_suggest_twice(self):
        """ Calling suggest twice returns two different jobs. """

        name = 'test ' + str(time())
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=default_parameters,
                                       outcome=default_outcome)

        a = scientist.suggest()
        sleep(2)
        b = scientist.suggest()
        
        # Two suggested jobs are different
        assert( cmp(a,b) != 0 )
        
        whetlab.delete_experiment(default_access_token,name) 


    def test_suggest(self):
        """ Suggest return a valid job. """

        name = 'test ' + str(time())
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=default_parameters,
                                       outcome=default_outcome)

        a = scientist.suggest()

        # Check all parameter names are valid in suggestion
        for k in a.keys():
            assert(k in default_parameters.keys())

        # Check if all parameters were assigned a value
        for k in default_parameters.keys():
            assert(k in a)

        # Check parameter values are within the min/max bounds
        for k,v in a.items():
            assert(v >= default_parameters[k]['min'])
            assert(v <= default_parameters[k]['max'])

        # Check parameter values are of right type
        for k,v in a.items():
            if default_parameters[k]['type'] == 'integer':
                assert(type(v) == int)
            if default_parameters[k]['type'] == 'float':
                assert(type(v) == float)
        
        whetlab.delete_experiment(default_access_token,name) 

    def test_best(self):
        """ Best returns the best job. """

        name = 'test ' + str(time())
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=default_parameters,
                                       outcome=default_outcome)

        scientist.update({'p1':1.,'p2':4},1)
        scientist.update({'p1':4.,'p2':2},2)
        scientist.update({'p1':5.,'p2':1},1000)
        scientist.update({'p1':9.,'p2':9},3)
        scientist.update({'p1':1.,'p2':1},4)
        scientist.update({'p1':5.,'p2':5},5)

        assert(cmp(scientist.best(),{'p1':5.,'p2':1})==0)

        whetlab.delete_experiment(default_access_token,name) 

    def test_pending(self):
        """ Pending returns jobs that have not been updated. """

        name = 'test ' + str(time())
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=default_parameters,
                                       outcome=default_outcome)

        a = scientist.suggest()
        b = scientist.suggest()
        c = scientist.suggest()
        scientist.update(b,10)
        l = scientist.pending()

        assert(a in l)
        assert(b not in l)
        assert(c in l)
        assert(len(l) == 2)

        whetlab.delete_experiment(default_access_token,name) 

    def test_clear_pending(self):
        """ Should remove pending jobs only. """

        name = 'test ' + str(time())
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=default_parameters,
                                       outcome=default_outcome)

        a = scientist.suggest()
        b = scientist.suggest()
        c = scientist.suggest()
        scientist.update(b,10)
        scientist.clear_pending()

        assert( len(scientist.pending()) == 0 )

        # Make sure only result left is "b"
        scientist._sync_with_server()
        print scientist._ids_to_param_values
        assert( cmp(scientist._ids_to_param_values.values()[0],b) == 0 )
        assert( cmp(scientist._ids_to_outcome_values.values()[0],10) == 0 )

        whetlab.delete_experiment(default_access_token,name) 


    @raises(ValueError)
    def test_update_parameter_too_small(self):
        """ Update should raise error if parameter smaller than minimum. """

        name = 'test ' + str(time())
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=default_parameters,
                                       outcome=default_outcome)

        scientist.update({'p1':-5.,'p2':5},5)

    @raises(ValueError)
    def test_update_parameter_too_big(self):
        """ Update should raise error if parameter larger than maximum. """

        name = 'test ' + str(time())
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=default_parameters,
                                       outcome=default_outcome)

        scientist.update({'p1':5.,'p2':50},5)

    @raises(TypeError)
    def test_update_parameter_not_integer(self):
        """ Update should raise error if an integer parameter has a non-integer value. """

        name = 'test ' + str(time())
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=default_parameters,
                                       outcome=default_outcome)

        scientist.update({'p1':5.,'p2':1.},5)

    @raises(TypeError)
    def test_update_parameter_not_float(self):
        """ Update should raise error if a float parameter has a non-float value. """

        name = 'test ' + str(time())
        scientist = whetlab.Experiment(access_token=default_access_token,
                                       name=name,
                                       description=default_description,
                                       parameters=default_parameters,
                                       outcome=default_outcome)

        scientist.update({'p1':5,'p2':1},5)
