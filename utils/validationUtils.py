





#check for fields missing in forms.  If they are missing, return that shiznit. 
def check_fields(needed, data):
	print data
	if data is None:
		raise Exception('woah')
	missing = list(set(needed)-set(data.keys()))
	for item in needed:
		if data[item]=='':
			if item not in missing:
				missing.append(item)
	missing = ','.join(missing)
	if (len(missing)>0):
		raise Exception('Missing fields: [%s]'% (missing))
