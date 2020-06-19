# Python Fast library for matching MQTT patterns with named wildcards to extract data from topics

SEPARATOR = "/"
SINGLE = "+"
ALL = "#"

def exec(pattern,topic):
  if matches(pattern,topic):
    return extract(pattern,topic)
  else:
    return 0

def matches(pattern,topic):
  patternSegments = pattern.split(SEPARATOR)
  topicSegments = topic.split(SEPARATOR)
  patternLength = len(patternSegments)
  topicLength = len(topicSegments)
  lastIndex = patternLength - 1
  for i in range(0, patternLength):
    currentPattern = patternSegments[i]
    if len(currentPattern):
      patternChar = currentPattern[0]
      currentTopic = topicSegments[i]
      if not currentTopic and currentPattern != ALL:
        return False
      if patternChar == ALL:
        return i == lastIndex
      if patternChar != SINGLE and currentPattern != currentTopic:
        return False

  return patternLength == topicLength

def extract(pattern,topic):
  params = {}
  patternSegments = pattern.split(SEPARATOR)
  topicSegments = topic.split(SEPARATOR)
  patternLength = len(patternSegments)
  for i in range(0, patternLength):
    currentPattern = patternSegments[i]
    if len(currentPattern):
      patternChar = currentPattern[0]
      if len(currentPattern) > 1:
        if patternChar == ALL:
          params[currentPattern[1:]] = topicSegments[i:]
          break
        elif patternChar == SINGLE:
          params[currentPattern[1:]] = topicSegments[i]
  return params