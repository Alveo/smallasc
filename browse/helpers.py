from collections import namedtuple
from browse.modelspackage.participants import Participant
from browse.modelspackage.sessions import Session
from browse.modelspackage.residence_history import ResidenceHistory
from browse.modelspackage.language_usage import LanguageUsage

ParticipantInfo = namedtuple('ParticipantInfo', 'participant sessions residential_history languages_spoken')

def get_participant_info(participant_id):
  participant = Participant.objects.get(participant_id)
  if not participant is None:
    sessions = Session.objects.filter_by_participant(participant) 
    rhist = ResidenceHistory.objects.filter_by_participant(participant)
    lang = LanguageUsage.objects.filter_by_participant(participant)

  return ParticipantInfo(participant = participant, 
                        sessions = sessions, 
                        residential_history = rhist, 
                        languages_spoken = lang)