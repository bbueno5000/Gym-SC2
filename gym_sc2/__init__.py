from gym.envs.registration import register

register(
    entry_point='gym_sc2.envs:SC2Env',
    id='BuildMarines-bbueno5000-v0',
    kwargs={'map_name': 'BuildMarines'})

register(
    entry_point='gym_sc2.envs:SC2Env',
    id='CollectMineralShards-bbueno5000-v0',
    kwargs={'map_name': 'CollectMineralShards'})

register(
    entry_point='gym_sc2.envs:SC2Env',
    id='CollectMineralsAndGas-bbueno5000-v0',
    kwargs={'map_name': 'CollectMineralsAndGas'})

register(
    entry_point='gym_sc2.envs:SC2Env',
    id='DefeatRoaches-bbueno5000-v0',
    kwargs={'map_name': 'DefeatRoaches'})

register(
    entry_point='gym_sc2.envs:SC2Env',
    id='DefeatZerglingsAndBanelings-bbueno5000-v0',
    kwargs={'map_name': 'DefeatZerglingsAndBanelings'})

register(
    entry_point='gym_sc2.envs:SC2Env',
    id='FindAndDefeatZerglings-bbueno5000-v0',
    kwargs={'map_name': 'FindAndDefeatZerglings'})

register(
    entry_point='gym_sc2.envs:SC2Env',
    id='MoveToBeacon-bbueno5000-v0',
    kwargs={'map_name': 'MoveToBeacon'})
