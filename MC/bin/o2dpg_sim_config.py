def create_sim_config(args):
    # creates a generic simulation config
    # based on arguments args (run number, energy, ...) originally passed
    # to o2dpg_sim_workflow.py

    COLTYPEIR = args.col
    if args.embedding==True:
        COLTYPEIR = args.colBkg

    config = {}
    def add(cfg, flatconfig):
       for entry in flatconfig:
           mk = entry.split(".")[0]
           sk = entry.split(".")[1]
           d = cfg.get(mk,{})
           d[sk] = flatconfig[entry]
           cfg[mk] = d

    # some specific settings for pp productions
    if COLTYPEIR == 'pp':
       # Alpide chip settings
       add(config, {"MFTAlpideParam.roFrameLengthInBC" : 198})
       if 302000 <= int(args.run) and int(args.run) < 309999:
           add(config, {"ITSAlpideParam.roFrameLengthInBC" : 198})

       # ITS reco settings
       add(config, {"ITSVertexerParam.phiCut" : 0.5,
                    "ITSVertexerParam.clusterContributorsCut" : 3,
                    "ITSVertexerParam.tanLambdaCut" : 0.2})
       # primary vertexing settings
       if 301000 <= int(args.run) and int(args.run) <= 301999:
          add(config, {"pvertexer.acceptableScale2" : 9,
                       "pvertexer.minScale2" : 2.,
                       "pvertexer.nSigmaTimeTrack" : 4.,
                       "pvertexer.timeMarginTrackTime" : 0.5,
                       "pvertexer.timeMarginVertexTime" : 7.,
                       "pvertexer.nSigmaTimeCut" : 10,
                       "pvertexer.dbscanMaxDist2" : 36,
                       "pvertexer.dcaTolerance" : 3.,
                       "pvertexer.pullIniCut" : 100,
                       "pvertexer.addZSigma2" : 0.1,
                       "pvertexer.tukey" : 20.,
                       "pvertexer.addZSigma2Debris" : 0.01,
                       "pvertexer.addTimeSigma2Debris" : 1.,
                       "pvertexer.maxChi2Mean" : 30,
                       "pvertexer.timeMarginReattach" : 3.,
                       "pvertexer.addTimeSigma2Debris" : 1.,
                       "pvertexer.dbscanDeltaT" : 24,
                       "pvertexer.maxChi2TZDebris" : 100,
                       "pvertexer.maxMultRatDebris" : 1.,
                       "pvertexer.dbscanAdaptCoef" : 20.})
       elif 302000 <= int(args.run) and int(args.run) <= 309999:
          # specific tunes for high pp
          # run range taken from https://twiki.cern.ch/twiki/bin/viewauth/ALICE/O2DPGMCSamplingSchema
          # taken from JIRA https://alice.its.cern.ch/jira/browse/O2-2691
          add(config, {"pvertexer.dbscanDeltaT" : 7,
                       "pvertexer.maxChi2TZDebris": 50,
                       "pvertexer.maxMultRatDebris": 1.,
                       "pvertexer.dbscanAdaptCoef" : 20,
                       "pvertexer.maxVerticesPerCluster" : 20,
                       "pvertexer.dbscanMaxDist2" : 36})

       else:
          # generic pp
          add(config, {"pvertexer.acceptableScale2" : 9,
                       "pvertexer.dbscanMaxDist2" : 36,
                       "pvertexer.dbscanDeltaT" : 24,
                       "pvertexer.maxChi2TZDebris" : 100,
                       "pvertexer.maxMultRatDebris" : 1.,
                       "pvertexer.dbscanAdaptCoef" : 20.})

    # MFT tracking settings
    if args.mft_reco_full == True:
        add(config, {"MFTTracking.forceZeroField" : 0,
                     "MFTTracking.LTFclsRCut" : 0.0100})

    return config
