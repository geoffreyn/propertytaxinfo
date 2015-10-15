from flask import Flask
from requests import Session

app = Flask(__name__)

@app.route("/sdat/<path:identifier>")
@app.route("/sdat")
def property_sdat_render(identifier):

    idpath = str(identifier).split('/')
    
    if len(idpath) <= 0 or len(idpath) > 2:
        error = ('Invalid identifiers specified: %s, length %i not correct.  \nProper usage: sdat/homeAddress (spaces alowed (NOT IMPLEMENTED!)) or sdat/block/lot are the only acceptable formats.') % (','.join(idpath),len(idpath))
        return error
    elif len(idpath) == 1:
        homeAddress = idpath[0]
        block = ''
        lot = ''
    else:
        block = idpath[0]
        lot = idpath[1]
        homeAddress = ''
        
    # Format boilerplate request
    formdict = {'ctl00$ctl00$ctl00$ToolkitScriptManager1':'ctl00$ctl00$ctl00$MainContent$MainContent$cphMainContentArea$ucSearchType$updatePanel1|ctl00$ctl00$ctl00$MainContent$MainContent$cphMainContentArea$ucSearchType$wzrdRealPropertySearch$StepNavigationTemplateContainerID$btnStepNextButton',
        'ctl00$ctl00$ctl00$MainContent$MainContent$cphMainContentArea$ucSearchType$hideBanner':'false',
        '__EVENTTARGET':'',
        '__EVENTARGUMENT':'',
        '__LASTFOCUS':'',
        '__VIEWSTATE':'/wEPDwUKLTI3NzgyMTg5Mw9kFgJmD2QWAmYPZBYCZg9kFgQCAQ9kFggCCQ8VAz0vUmVhbFByb3BlcnR5L2Vnb3YvZnJhbWV3b3Jrcy9ib290c3RyYXAvY3NzL2Jvb3RzdHJhcC5taW4uY3NzKC9SZWFsUHJvcGVydHkvZWdvdi9jc3MvYWdlbmN5LXN0eWxlcy5jc3M1L1JlYWxQcm9wZXJ0eS9lZ292L2Nzcy9tZGdvdl9yZXNwb25zaXZlVGFibGVzLm1pbi5jc3NkAgoPZBYCZg8VASgvUmVhbFByb3BlcnR5L2Vnb3YvY3NzL2FnZW5jeS1oZWFkZXIuY3NzZAILDxUKIS9SZWFsUHJvcGVydHkvZWdvdi9jc3MvaWUvaWU4LmNzcyEvUmVhbFByb3BlcnR5L2Vnb3YvY3NzL2llL2llNy5jc3MiL1JlYWxQcm9wZXJ0eS9lZ292L2pzL2h0bWw1c2hpdi5qcxsvUmVhbFByb3BlcnR5L2Nzcy9wcmludC5jc3MfL1JlYWxQcm9wZXJ0eS9zY3JpcHRzL2dsb2JhbC5qcykvUmVhbFByb3BlcnR5L2Vnb3YvanMvanF1ZXJ5LTEuOC4yLm1pbi5qcykvUmVhbFByb3BlcnR5L3NjcmlwdHMvanF1ZXJ5LmN5Y2xlLmFsbC5qcygvUmVhbFByb3BlcnR5L3NjcmlwdHMvanF1ZXJ5LnZhbGlkYXRlLmpzGi9SZWFsUHJvcGVydHkvSlMvZ2xvYmFsLmpzIC9SZWFsUHJvcGVydHkvZWdvdi9qcy95dWktbWluLmpzZAIMD2QWAgIBD2QWAmYPFQIaL1JlYWxQcm9wZXJ0eS9DU1MvTWFpbi5jc3MgL1JlYWxQcm9wZXJ0eS9jc3MvVGFibGVTdHlsZS5jc3NkAgMPZBYKAgEPZBYCAgEPFgIeBGhyZWYFHGh0dHA6Ly93d3cuZGF0Lm1hcnlsYW5kLmdvdi8WAgIBDxYEHgNzcmMFGX4vZWdvdi9pbWcvU0RBVF9USVRMRS5wbmceA2FsdAU1TWFyeWxhbmQgU3RhdGUgRGVwYXJ0bWVudCBvZiBBc3Nlc3NtZW50cyBhbmQgVGF4YXRpb25kAgMPZBYCAgEPZBYEAgMPZBYCAgEPDxYCHgRUZXh0BQJ3M2RkAgUPZBYCAgEPZBYCZg9kFgJmD2QWBgIFD2QWBAIBDw8WAh8DZWRkAgMPEGRkFgBkAgcPPCsADwEOaBYCZg9kFgICAQ9kFgJmD2QWAmYPZBYKZg9kFgICAQ9kFgJmD2QWAgIBD2QWBAIDDxAPFgYeDURhdGFUZXh0RmllbGQFBXZhbHVlHg5EYXRhVmFsdWVGaWVsZAUDa2V5HgtfIURhdGFCb3VuZGdkEBUZDC1TZWxlY3Qgb25lLQ9BTExFR0FOWSBDT1VOVFkTQU5ORSBBUlVOREVMIENPVU5UWQ5CQUxUSU1PUkUgQ0lUWRBCQUxUSU1PUkUgQ09VTlRZDkNBTFZFUlQgQ09VTlRZD0NBUk9MSU5FIENPVU5UWQ5DQVJST0xMIENPVU5UWQxDRUNJTCBDT1VOVFkOQ0hBUkxFUyBDT1VOVFkRRE9SQ0hFU1RFUiBDT1VOVFkQRlJFREVSSUNLIENPVU5UWQ5HQVJSRVRUIENPVU5UWQ5IQVJGT1JEIENPVU5UWQ1IT1dBUkQgQ09VTlRZC0tFTlQgQ09VTlRZEU1PTlRHT01FUlkgQ09VTlRZFlBSSU5DRSBHRU9SR0UnUyBDT1VOVFkTUVVFRU4gQU5ORSdTIENPVU5UWRFTVC4gTUFSWSdTIENPVU5UWQ9TT01FUlNFVCBDT1VOVFkNVEFMQk9UIENPVU5UWRFXQVNISU5HVE9OIENPVU5UWQ9XSUNPTUlDTyBDT1VOVFkQV09SQ0VTVEVSIENPVU5UWRUZAi0xAjAxAjAyAjAzAjA0AjA1AjA2AjA3AjA4AjA5AjEwAjExAjEyAjEzAjE0AjE1AjE2AjE3AjE4AjE5AjIwAjIxAjIyAjIzAjI0FCsDGWdnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2cWAQIDZAIJDxAPFgYfBAUFdmFsdWUfBQUDa2V5HwZnZBAVBQwtU2VsZWN0IG9uZS0OU1RSRUVUIEFERFJFU1MbUFJPUEVSVFkgQUNDT1VOVCBJREVOVElGSUVSCk1BUC9QQVJDRUwOUFJPUEVSVFkgU0FMRVMVBQItMQIwMQIwMgIwMwIwNBQrAwVnZ2dnZxYBAgNkAgEPZBYCAgEPZBYGAgEPDxYCHwMFJkVudGVyIE1hcCBSZWZlcmVuY2UgZm9yIEJBTFRJTU9SRSBDSVRZZGQCBw8WAh4HVmlzaWJsZWdkAg0PZBYSAgMPEGQPFg1m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dGwwMCRjdGwwMCRNYWluQ29udGVudCRNYWluQ29udGVudCRjcGhNYWluQ29udGVudEFyZWEkdWNTZWFyY2hUeXBlJHd6cmRSZWFsUHJvcGVydHlTZWFyY2gkdWNTZWFyY2hSZXN1bHQkZ3ZfU2VhcmNoQnlSUFNhbGUPZ2QFhAFjdGwwMCRjdGwwMCRjdGwwMCRNYWluQ29udGVudCRNYWluQ29udGVudCRjcGhNYWluQ29udGVudEFyZWEkdWNTZWFyY2hUeXBlJHd6cmRSZWFsUHJvcGVydHlTZWFyY2gkdWNHcm91bmRSZW50JGd2X0dSUmVnaXN0cmF0b25SZXN1bHQPZ2QFYGN0bDAwJGN0bDAwJGN0bDAwJE1haW5Db250ZW50JE1haW5Db250ZW50JGNwaE1haW5Db250ZW50QXJlYSR1Y1NlYXJjaFR5cGUkd3pyZFJlYWxQcm9wZXJ0eVNlYXJjaA8QZBQrAQICAWYCAWQFcGN0bDAwJGN0bDAwJGN0bDAwJE1haW5Db250ZW50JE1haW5Db250ZW50JGNwaE1haW5Db250ZW50QXJlYSR1Y1NlYXJjaFR5cGUkd3pyZFJlYWxQcm9wZXJ0eVNlYXJjaCRXaXphcmRNdWx0aVZpZXcPD2QCAWQFf2N0bDAwJGN0bDAwJGN0bDAwJE1haW5Db250ZW50JE1haW5Db250ZW50JGNwaE1haW5Db250ZW50QXJlYSR1Y1NlYXJjaFR5cGUkd3pyZFJlYWxQcm9wZXJ0eVNlYXJjaCR1Y1NlYXJjaFJlc3VsdCRndl9TZWFyY2hSZXN1bHQPZ2QiKe/maufK7R523/kR+li5nB83xw==',
        '__VIEWSTATEGENERATOR':'67B65B95',
        '__EVENTVALIDATION':'/wEdAAeLHO4UiazhjJoEWt6WhsuhTM7lR6wkAQA4/LrX3F8+kJFCX6GXNshSNYudQwBINupfx21Q/fwirSrEZb/6IfokQ2/ExUnKIexbtLnm+FwTUQqLyXAQIRgTGoe+xG2l1j+MyhVtrGKhaCDPE00ZGRUyHazg9c4YiKfaisSIpUPyWMst3r0=',
        '__ASYNCPOST':'true',
        'ctl00$ctl00$ctl00$MainContent$MainContent$cphMainContentArea$ucSearchType$wzrdRealPropertySearch$StepNavigationTemplateContainerID$btnStepNextButton':'Next',
        }
    
    # Site requires only specific fields are filled, e.g., if block and lot are available, clear the Address field
    if block != '' and lot != '':
        formdict['ctl00$ctl00$ctl00$MainContent$MainContent$cphMainContentArea$ucSearchType$wzrdRealPropertySearch$ucEnterData$txtMap_Block'] = block
        formdict['ctl00$ctl00$ctl00$MainContent$MainContent$cphMainContentArea$ucSearchType$wzrdRealPropertySearch$ucEnterData$txtMap_Lot'] = lot
        
    ## NOT FUNCTIONAL!
    elif homeAddress != '':
        formdict['ctl00$ctl00$ctl00$MainContent$MainContent$cphMainContentArea$ucSearchType$wzrdRealPropertySearch$ucEnterData$txtStreenNumber'] = homeAddress.split('%20')[0]
        formdict['ctl00$ctl00$ctl00$MainContent$MainContent$cphMainContentArea$ucSearchType$wzrdRealPropertySearch$ucEnterData$txtStreetName'] = ' '.join(homeAddress.split('%20')[1:])
        
        
    session = Session()

    # HEAD requests ask for *just* the headers, which is all you need to grab the
    # session cookie
    session.head('http://sdat.dat.maryland.gov/RealProperty/Pages')

    response = session.post('http://sdat.dat.maryland.gov/RealProperty/Pages/default.aspx',
        data = formdict
    )
        
    # Output rendered HTML page to file in current directory
    #with open('propinfo.html','wb') as f:
    #	f.write(response.text.encode('utf-8'))	
            
    return response.text.encode('utf-8')
	
    

@app.route("/tax/<path:identifier>")
@app.route("/tax")
def property_info_render(identifier):

    idpath = str(identifier).split('/')
    
    if len(idpath) <= 0 or len(idpath) > 2:
        error = ('Invalid identifiers specified: length %i not correct.  \nProper usage: tax/homeAddress (spaces alowed) or tax/block/lot are the only acceptable formats.' % len(idpath))
    #     return error
    elif len(idpath) == 1:
        homeAddress = idpath[0]
        block = ''
        lot = ''
    else:
        block = idpath[0]
        lot = idpath[1]
        homeAddress = ''
    
    # Format boilerplate request
    formdict = {}
    
    formdict['__EVENTTARGET'] = 'ctl00$ctl00$rootMasterContent$LocalContentPlaceHolder$DataGrid1$ctl02$lnkBtnSelect'
    formdict['__VIEWSTATE'] = '/wEPDwUKMTQ5MjEyMzA1OA8WAh4FWWVhcnMVBAQyMDE2BDIwMTUEMjAxNAQyMDEzFgJmD2QWAmYPZBYEZg9kFgQCAg8WAh4EVGV4dGVkAgUPFgIeB1Zpc2libGVnFgJmDxYCHwFlZAIBD2QWCgIBDw8WAh4ISW1hZ2VVcmwFVmh0dHA6Ly9jaXR5c2VydmljZXMuYmFsdGltb3JlY2l0eS5nb3YvcmVtb3RlbWFzdGVydjMvaW1hZ2VzL2ludGVybmV0L2ljb25zL2xvYWRpbmcuZ2lmZGQCBA8WAh8CZ2QCBg8WAh8CZxYCAgEPFgIfAQUNUmVhbCBQcm9wZXJ0eWQCBw9kFggCAQ9kFgICAQ9kFgRmDw8WBh8BBRJTZWFyY2ggVW5hdmFpbGFibGUeB1Rvb2xUaXAFOFNlYXJjaCBpcyBjdXJyZW50bHkgdW5hdmFpbGFibGUsIHBsZWFzZSB0cnkgYWdhaW4gbGF0ZXIuHghSZWFkT25seWcWBB4Hb25mb2N1cwUxaWYodGhpcy52YWx1ZT09J0tleXdvcmQgb3IgU2VhcmNoJyl0aGlzLnZhbHVlPScnOx4Gb25ibHVyBTFpZih0aGlzLnZhbHVlPT0nJyl0aGlzLnZhbHVlPSdLZXl3b3JkIG9yIFNlYXJjaCc7ZAIBDw8WAh4HRW5hYmxlZGgWAh4Hb25jbGljawVoaWYoZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ2N0bDAwX2N0bDAwX3R4dEdvb2dsZUN1c3RvbVNlYXJjaCcpLnZhbHVlPT0nS2V5d29yZCBvciBTZWFyY2gnKXJldHVybiBmYWxzZTtkAgIPZBYEAgEPFgIfAQUMRmluYW5jZSBNZW51ZAIDDxQrAAIUKwACDxYGHgtfIURhdGFCb3VuZGceF0VuYWJsZUFqYXhTa2luUmVuZGVyaW5naB4MRGF0YVNvdXJjZUlEBRJTaXRlTWFwRGF0YVNvdXJjZTFkDxQrABMUKwACDxYIHwEFBEhvbWUeC05hdmlnYXRlVXJsBTlodHRwOi8vd3d3LmJhbHRpbW9yZWNpdHkuZ292L2dvdmVybm1lbnQvZmluYW5jZS9pbmRleC5waHAeBVZhbHVlBQRIb21lHwQFBEhvbWVkZBQrAAIPFggfAQUUQWNjb3VudGluZyAmIFBheXJvbGwfDQU7aHR0cDovL3d3dy5iYWx0aW1vcmVjaXR5Lmdvdi9nb3Zlcm5tZW50L2ZpbmFuY2UvYWNjb3VudC5waHAfDgUUQWNjb3VudGluZyAmIFBheXJvbGwfBAUUQWNjb3VudGluZyAmIFBheXJvbGxkZBQrAAIPFggfAQUcQnVkZ2V0ICYgTWFuYWdlbWVudCBSZXNlYXJjaB8NBThodHRwOi8vd3d3LmJhbHRpbW9yZWNpdHkuZ292L2dvdmVybm1lbnQvZmluYW5jZS9iYm1yLnBocB8OBRxCdWRnZXQgJiBNYW5hZ2VtZW50IFJlc2VhcmNoHwQFHEJ1ZGdldCAmIE1hbmFnZW1lbnQgUmVzZWFyY2hkZBQrAAIPFggfAQUJUHVyY2hhc2VzHw0FPWh0dHA6Ly93d3cuYmFsdGltb3JlY2l0eS5nb3YvZ292ZXJubWVudC9maW5hbmNlL3B1cmNoYXNlcy5waHAfDgUJUHVyY2hhc2VzHwQFCVB1cmNoYXNlc2RkFCsAAg8WCB8BBQ9SaXNrIE1hbmFnZW1lbnQfDQU8aHR0cDovL3d3dy5iYWx0aW1vcmVjaXR5Lmdvdi9nb3Zlcm5tZW50L2ZpbmFuY2Uvcmlza21nbXQucGhwHw4FD1Jpc2sgTWFuYWdlbWVudB8EBQ9SaXNrIE1hbmFnZW1lbnRkZBQrAAIPFggfAQUTVHJlYXN1cnkgTWFuYWdlbWVudB8NBTxodHRwOi8vd3d3LmJhbHRpbW9yZWNpdHkuZ292L2dvdmVybm1lbnQvZmluYW5jZS90cmVhc3VyeS5waHAfDgUTVHJlYXN1cnkgTWFuYWdlbWVudB8EBRNUcmVhc3VyeSBNYW5hZ2VtZW50ZGQUKwACDxYIHwEFE1JldmVudWUgQ29sbGVjdGlvbnMfDQU7aHR0cDovL3d3dy5iYWx0aW1vcmVjaXR5Lmdvdi9nb3Zlcm5tZW50L2ZpbmFuY2UvcmV2ZW51ZS5waHAfDgUTUmV2ZW51ZSBDb2xsZWN0aW9ucx8EBRNSZXZlbnVlIENvbGxlY3Rpb25zZGQUKwACDxYIHwEFE0RvY3VtZW50cyAmIFJlcG9ydHMfDQU4aHR0cDovL3d3dy5iYWx0aW1vcmVjaXR5Lmdvdi9nb3Zlcm5tZW50L2ZpbmFuY2UvZG9jcy5waHAfDgUTRG9jdW1lbnRzICYgUmVwb3J0cx8EBRNEb2N1bWVudHMgJiBSZXBvcnRzZGQUKwACDxYIHwEFD09ubGluZSBQYXltZW50cx8NBS1odHRwOi8vY2l0eXNlcnZpY2VzLmJhbHRpbW9yZWNpdHkuZ292L3BheXN5cy8fDgUPT25saW5lIFBheW1lbnRzHwQFD09ubGluZSBQYXltZW50c2RkFCsAAg8WCB8BBRM8aDI+RkFRIC8gSGVscDwvaDI+Hw0FDy9SZWFsUHJvcGVydHkvIx8OBRM8aDI+RkFRIC8gSGVscDwvaDI+HwRlZGQUKwACDxYIHwEFDVRheCBTYWxlIEZBUXMfDQUbaHR0cDovL3d3dy5iaWRiYWx0aW1vcmUuY29tHw4FDVRheCBTYWxlIEZBUXMfBAUNVGF4IFNhbGUgRkFRc2RkFCsAAg8WCB8BBRFQYXJraW5nIEZpbmVzIEZBUR8NBUFodHRwOi8vd3d3LmJhbHRpbW9yZWNpdHkuZ292L2Fuc3dlcnMvaW5kZXgucGhwP2FjdGlvbj1zaG93JmNhdD0xMB8OBRFQYXJraW5nIEZpbmVzIEZBUR8EBRFQYXJraW5nIEZpbmVzIEZBUWRkFCsAAg8WCB8BBRFSZWFsIFByb3BlcnR5IEZBUR8NBUFodHRwOi8vd3d3LmJhbHRpbW9yZWNpdHkuZ292L2Fuc3dlcnMvaW5kZXgucGhwP2FjdGlvbj1zaG93JmNhdD0xMh8OBRFSZWFsIFByb3BlcnR5IEZBUR8EBRFSZWFsIFByb3BlcnR5IEZBUWRkFCsAAg8WCB8BBRVQYXJraW5nIEZpbmVzIExpc3RpbmcfDQVraHR0cDovL3d3dy5iYWx0aW1vcmVjaXR5Lmdvdi9nb3Zlcm5tZW50L3RyYW5zcG9ydGF0aW9uL2Rvd25sb2Fkcy8xMjA3LzEyMTkwNyBQYXJraW5nIEZpbmVzIExpc3RpbmcgMjAwNy5wZGYfDgUVUGFya2luZyBGaW5lcyBMaXN0aW5nHwQFFVBhcmtpbmcgRmluZXMgTGlzdGluZ2RkFCsAAg8WCB8BBRhBdm9pZGluZyBQYXJraW5nIFRpY2tldHMfDQVoaHR0cDovL3d3dy5iYWx0aW1vcmVjaXR5Lmdvdi9nb3Zlcm5tZW50L3RyYW5zcG9ydGF0aW9uL2Rvd25sb2Fkcy8xMjA3LzEyMTkwNyBQYXJraW5nIFRpY2tldCBCcm9jaHVyZS5wZGYfDgUYQXZvaWRpbmcgUGFya2luZyBUaWNrZXRzHwQFGEF2b2lkaW5nIFBhcmtpbmcgVGlja2V0c2RkFCsAAg8WCB8BBRFUcmFuc2ZlciBUYXggVW5pdB8NBUFodHRwOi8vd3d3LmJhbHRpbW9yZWNpdHkuZ292L2Fuc3dlcnMvaW5kZXgucGhwP2FjdGlvbj1zaG93JmNhdD0xMR8OBRFUcmFuc2ZlciBUYXggVW5pdB8EBRFUcmFuc2ZlciBUYXggVW5pdGRkFCsAAg8WCB8BBQpMaWVucyBVbml0Hw0FPWh0dHA6Ly93d3cuYmFsdGltb3JlY2l0eS5nb3YvZ292ZXJubWVudC9maW5hbmNlL2ZhcXRsaWVucy5waHAfDgUKTGllbnMgVW5pdB8EBQpMaWVucyBVbml0ZGQUKwACDxYIHwEFF0xpZW4gQ2VydGlmaWNhdGUgUG9saWN5Hw0FX2h0dHA6Ly93d3cuYmFsdGltb3JlY2l0eS5nb3YvZ292ZXJubWVudC9maW5hbmNlL2ltYWdlcy9MaWVuIENlcnRpZmljYXRlIHBvbGljeSBfMl8gT2N0IDIwMDgucGRmHw4FF0xpZW4gQ2VydGlmaWNhdGUgUG9saWN5HwQFF0xpZW4gQ2VydGlmaWNhdGUgUG9saWN5ZGQUKwACDxYIHwEFCENvbnRhY3RzHw1lHw4FCENvbnRhY3RzHwRlZGQPFCsBE2ZmZmZmZmZmZmZmZmZmZmZmZmYWAQVzVGVsZXJpay5XZWIuVUkuUmFkTWVudUl0ZW0sIFRlbGVyaWsuV2ViLlVJLCBWZXJzaW9uPTIwMDguMi44MjYuMjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49MTIxZmFlNzgxNjViYTNkNGQWJmYPDxYIHwEFBEhvbWUfDQU5aHR0cDovL3d3dy5iYWx0aW1vcmVjaXR5Lmdvdi9nb3Zlcm5tZW50L2ZpbmFuY2UvaW5kZXgucGhwHw4FBEhvbWUfBAUESG9tZWRkAgEPDxYIHwEFFEFjY291bnRpbmcgJiBQYXlyb2xsHw0FO2h0dHA6Ly93d3cuYmFsdGltb3JlY2l0eS5nb3YvZ292ZXJubWVudC9maW5hbmNlL2FjY291bnQucGhwHw4FFEFjY291bnRpbmcgJiBQYXlyb2xsHwQFFEFjY291bnRpbmcgJiBQYXlyb2xsZGQCAg8PFggfAQUcQnVkZ2V0ICYgTWFuYWdlbWVudCBSZXNlYXJjaB8NBThodHRwOi8vd3d3LmJhbHRpbW9yZWNpdHkuZ292L2dvdmVybm1lbnQvZmluYW5jZS9iYm1yLnBocB8OBRxCdWRnZXQgJiBNYW5hZ2VtZW50IFJlc2VhcmNoHwQFHEJ1ZGdldCAmIE1hbmFnZW1lbnQgUmVzZWFyY2hkZAIDDw8WCB8BBQlQdXJjaGFzZXMfDQU9aHR0cDovL3d3dy5iYWx0aW1vcmVjaXR5Lmdvdi9nb3Zlcm5tZW50L2ZpbmFuY2UvcHVyY2hhc2VzLnBocB8OBQlQdXJjaGFzZXMfBAUJUHVyY2hhc2VzZGQCBA8PFggfAQUPUmlzayBNYW5hZ2VtZW50Hw0FPGh0dHA6Ly93d3cuYmFsdGltb3JlY2l0eS5nb3YvZ292ZXJubWVudC9maW5hbmNlL3Jpc2ttZ210LnBocB8OBQ9SaXNrIE1hbmFnZW1lbnQfBAUPUmlzayBNYW5hZ2VtZW50ZGQCBQ8PFggfAQUTVHJlYXN1cnkgTWFuYWdlbWVudB8NBTxodHRwOi8vd3d3LmJhbHRpbW9yZWNpdHkuZ292L2dvdmVybm1lbnQvZmluYW5jZS90cmVhc3VyeS5waHAfDgUTVHJlYXN1cnkgTWFuYWdlbWVudB8EBRNUcmVhc3VyeSBNYW5hZ2VtZW50ZGQCBg8PFggfAQUTUmV2ZW51ZSBDb2xsZWN0aW9ucx8NBTtodHRwOi8vd3d3LmJhbHRpbW9yZWNpdHkuZ292L2dvdmVybm1lbnQvZmluYW5jZS9yZXZlbnVlLnBocB8OBRNSZXZlbnVlIENvbGxlY3Rpb25zHwQFE1JldmVudWUgQ29sbGVjdGlvbnNkZAIHDw8WCB8BBRNEb2N1bWVudHMgJiBSZXBvcnRzHw0FOGh0dHA6Ly93d3cuYmFsdGltb3JlY2l0eS5nb3YvZ292ZXJubWVudC9maW5hbmNlL2RvY3MucGhwHw4FE0RvY3VtZW50cyAmIFJlcG9ydHMfBAUTRG9jdW1lbnRzICYgUmVwb3J0c2RkAggPDxYIHwEFD09ubGluZSBQYXltZW50cx8NBS1odHRwOi8vY2l0eXNlcnZpY2VzLmJhbHRpbW9yZWNpdHkuZ292L3BheXN5cy8fDgUPT25saW5lIFBheW1lbnRzHwQFD09ubGluZSBQYXltZW50c2RkAgkPDxYIHwEFEzxoMj5GQVEgLyBIZWxwPC9oMj4fDQUPL1JlYWxQcm9wZXJ0eS8jHw4FEzxoMj5GQVEgLyBIZWxwPC9oMj4fBGVkZAIKDw8WCB8BBQ1UYXggU2FsZSBGQVFzHw0FG2h0dHA6Ly93d3cuYmlkYmFsdGltb3JlLmNvbR8OBQ1UYXggU2FsZSBGQVFzHwQFDVRheCBTYWxlIEZBUXNkZAILDw8WCB8BBRFQYXJraW5nIEZpbmVzIEZBUR8NBUFodHRwOi8vd3d3LmJhbHRpbW9yZWNpdHkuZ292L2Fuc3dlcnMvaW5kZXgucGhwP2FjdGlvbj1zaG93JmNhdD0xMB8OBRFQYXJraW5nIEZpbmVzIEZBUR8EBRFQYXJraW5nIEZpbmVzIEZBUWRkAgwPDxYIHwEFEVJlYWwgUHJvcGVydHkgRkFRHw0FQWh0dHA6Ly93d3cuYmFsdGltb3JlY2l0eS5nb3YvYW5zd2Vycy9pbmRleC5waHA/YWN0aW9uPXNob3cmY2F0PTEyHw4FEVJlYWwgUHJvcGVydHkgRkFRHwQFEVJlYWwgUHJvcGVydHkgRkFRZGQCDQ8PFggfAQUVUGFya2luZyBGaW5lcyBMaXN0aW5nHw0Fa2h0dHA6Ly93d3cuYmFsdGltb3JlY2l0eS5nb3YvZ292ZXJubWVudC90cmFuc3BvcnRhdGlvbi9kb3dubG9hZHMvMTIwNy8xMjE5MDcgUGFya2luZyBGaW5lcyBMaXN0aW5nIDIwMDcucGRmHw4FFVBhcmtpbmcgRmluZXMgTGlzdGluZx8EBRVQYXJraW5nIEZpbmVzIExpc3RpbmdkZAIODw8WCB8BBRhBdm9pZGluZyBQYXJraW5nIFRpY2tldHMfDQVoaHR0cDovL3d3dy5iYWx0aW1vcmVjaXR5Lmdvdi9nb3Zlcm5tZW50L3RyYW5zcG9ydGF0aW9uL2Rvd25sb2Fkcy8xMjA3LzEyMTkwNyBQYXJraW5nIFRpY2tldCBCcm9jaHVyZS5wZGYfDgUYQXZvaWRpbmcgUGFya2luZyBUaWNrZXRzHwQFGEF2b2lkaW5nIFBhcmtpbmcgVGlja2V0c2RkAg8PDxYIHwEFEVRyYW5zZmVyIFRheCBVbml0Hw0FQWh0dHA6Ly93d3cuYmFsdGltb3JlY2l0eS5nb3YvYW5zd2Vycy9pbmRleC5waHA/YWN0aW9uPXNob3cmY2F0PTExHw4FEVRyYW5zZmVyIFRheCBVbml0HwQFEVRyYW5zZmVyIFRheCBVbml0ZGQCEA8PFggfAQUKTGllbnMgVW5pdB8NBT1odHRwOi8vd3d3LmJhbHRpbW9yZWNpdHkuZ292L2dvdmVybm1lbnQvZmluYW5jZS9mYXF0bGllbnMucGhwHw4FCkxpZW5zIFVuaXQfBAUKTGllbnMgVW5pdGRkAhEPDxYIHwEFF0xpZW4gQ2VydGlmaWNhdGUgUG9saWN5Hw0FX2h0dHA6Ly93d3cuYmFsdGltb3JlY2l0eS5nb3YvZ292ZXJubWVudC9maW5hbmNlL2ltYWdlcy9MaWVuIENlcnRpZmljYXRlIHBvbGljeSBfMl8gT2N0IDIwMDgucGRmHw4FF0xpZW4gQ2VydGlmaWNhdGUgUG9saWN5HwQFF0xpZW4gQ2VydGlmaWNhdGUgUG9saWN5ZGQCEg8PFggfAQUIQ29udGFjdHMfDWUfDgUIQ29udGFjdHMfBGVkZAIFDxYCHwEFETxoMj5DT05UQUNUUzwvaDI+ZAIGDxYCHwEFqwM8ZGl2IHN0eWxlPSdwYWRkaW5nOjEwcHg7Jz48YSBocmVmPSdtYWlsdG86QmFsdGltb3JlQ2l0eUNvbGxlY3Rpb25zQGJhbHRpbW9yZWNpdHkuZ292Jz48c3Ryb25nPlJldmVudWUgQ29sbGVjdGlvbnM8L3N0cm9uZz48L2E+PGJyLz4yMDAgSG9sbGlkYXkgU3QuLCBSb29tIDc8YnIvPjxici8+PGEgaHJlZj0naHR0cDovL3d3dy5iYWx0aW1vcmVjaXR5Lmdvdi9nb3Zlcm5tZW50L2ZpbmFuY2UvcmV2ZW51ZS5waHAjY29udGFjdHMnPjxzdHJvbmc+QWxsICBDb250YWN0IE51bWJlcnM8L3N0cm9uZz48L2E+PGJyLz48YnIgLz4gPGJyLz48aDE+QWRtaW5pc3RyYXRpb248L2gxPiA8YnIvPjxzdHJvbmc+IEhlbnJ5IFJheW1vbmQgIDxiciAvPiA8L3N0cm9uZz48ZW0+Q2hpZWY8L2VtPjxiciAvPkJ1cmVhdSBvZiBSZXZlbnVlIENvbGxlY3Rpb25zPC9kaXY+ZAIJD2QWAgIBD2QWEAIBDxYCHgRocmVmBTZodHRwOi8vY2l0eXNlcnZpY2VzLmJhbHRpbW9yZWNpdHkuZ292L1NwZWNpYWxCZW5lZml0cy9kAgIPDxYIHwEFbVRoZSBFWEVDVVRFIHBlcm1pc3Npb24gd2FzIGRlbmllZCBvbiB0aGUgb2JqZWN0ICdBZGRMb2dFbnRyeScsIGRhdGFiYXNlICdGaW5hbmNlX1JlYWxQcm9wZXJ0eScsIHNjaGVtYSAnZGJvJy4fAmgeCUZvcmVDb2xvcgqNAR4EXyFTQgIEZGQCAw8PFgIfAmhkFghmDxBkDxYEZgIBAgICAxYEEAUJMjAxNS8yMDE2BQQyMDE2ZxAFCTIwMTQvMjAxNQUEMjAxNWcQBQkyMDEzLzIwMTQFBDIwMTRnEAUJMjAxMi8yMDEzBQQyMDEzZxYBZmQCAQ8PFgIfAQUEMDAyMWRkAgIPDxYCHwEFAzAyMmRkAgYPDxYCHwJoZGQCBA8PFgIfAmhkFgICAQ8WAh8BBYAJPG9sPjxsaT5UaGlzIHBhZ2UgaXMgZm9yIFJlYWwgUHJvcGVydHkgdGF4ZXMuICBVc2UgdGhpcyBsaW5rIGZvciA8YSBocmVmPScvU3BlY2lhbEJlbmVmaXRzLyc+U3BlY2lhbCBCZW5lZml0IERpc3RyaWN0IFN1cmNoYXJnZXM8L2E+LiANCjxsaT5JZiB5b3Uga25vdyB0aGUgQmxvY2sgJiBMb3QsIGVudGVyIG9ubHkgdGhlIGJsb2NrICYgbG90LiANCjxsaT5JZiB5b3UgYXJlIHNlYXJjaGluZyBieSBwcm9wZXJ0eSBhZGRyZXNzIG9yIG93bmVyIG5hbWUsIHlvdSBtYXkgZW50ZXIgYW55IHBvcnRpb24gb2YgZWl0aGVyIG9yIGJvdGggb2YgdGhvc2UgZmllbGRzLiAgV2hlbiB5b3UgZW50ZXIgZGF0YSBpbiBhIHNlYXJjaCBmaWVsZCwgdGhlIGRhdGEgeW91IGVudGVyZWQgaXMgbG9va2VkIGZvciBhbnl3aGVyZSB3aXRoaW4gdGhhdCBmaWVsZC4gRm9yIGV4YW1wbGUsIGlmIHlvdSBlbnRlciBCbHVlIGluIHRoZSBBZGRyZXNzIGZpZWxkLCB5b3Ugd2lsbCBnZXQgcmVzdWx0cyBpbmNsdWRpbmcgQmx1ZWJlcnJ5LCBCbHVlYm9ubmV0LCBUcnVlQmx1ZSwgZXRjLiANCjxsaT5EaXJlY3Rpb25zIHN1Y2ggYXMgTm9ydGgsIFNvdXRoLCBFYXN0LCBXZXN0IHNob3VsZCBiZSBlbnRlcmVkIGFzIE4sUyxFLFcgd2l0aCBubyBwZXJpb2QuIA0KPGxpPklmIHlvdXIgc2VhcmNoIGZhaWxzLCByZXRyeSB3aXRoIGxlc3MgaW5mb3JtYXRpb24gc3VjaCBhcywgRmlyc3QgU2VhcmNoOiBPd25lcj1Sb3NlbmJsYXR0LCByZXN1bHRzPTAgU2Vjb25kIFNlYXJjaDogT3duZXI9Um9zZW4gcmVzdWx0cz0xMjQgDQo8bGk+TGVhdmUgb2ZmIGFsbCBzdHJlZXQgc3VmZml4ZXMgc3VjaCBhcyBTdC4sV2F5LCBSb2FkIGV0Yy4gDQo8bGk+V2hlbiBzZWFyY2hpbmcgYnkgbmFtZSwgZW50ZXIgaW4gTGFzdE5hbWUsIEZpcnN0TmFtZSBmb3JtYXQuIA0KPGxpPklmIGFsbCB5b3VyIHNlYXJjaGVzIGFyZSB1bnN1Y2Nlc3NmdWwsIHBsZWFzZSBjb250YWN0IHRoZSBEZXB0LiBvZiBGaW5hbmNlIGF0IDQxMC0zOTYtMzk4Nw0KPGxpPjxzdHJvbmc+UmV0dXJuZWQgc2VhcmNoIHJlc3VsdHMgYXJlIGxpbWl0ZWQgdG8gNTAgcmVjb3Jkcy4gSWYgeW91IHJlYWNoIHRoaXMgbGltaXQsIHBsZWFzZSByZWZpbmUgeW91ciBzZWFyY2ggY3JpdGVyaWEuPHN0cm9uZz4NCjwvb2w+ZAIFDw8WAh8CZ2QWCgIBDw8WBB8CZx8BBTE8Yj5Dcml0ZXJpYSBVc2VkOjwvYj5ZZWFyPTIwMTYgQmxvY2s9MDAyMSBMb3Q9MDIyZGQCAw8PFggfEAqQAR8BBRY8Yj5SZWNvcmRzIGZvdW5kOjwvYj4xHwJnHxECBGRkAgUPDxYEHwJnHwEFGTxiPlNvcnRlZCBCeTo8L2I+QmxvY2tMb3RkZAIHDw8WAh8CZ2RkAgkPPCsACwEADxYMHgtfIUl0ZW1Db3VudAIBHghEYXRhS2V5cxYBBQkwMDIxIDAyMiAeDERhdGFLZXlGaWVsZAUIYmxvY2tsb3QeCVBhZ2VDb3VudAIBHhVfIURhdGFTb3VyY2VJdGVtQ291bnQCAR4QQ3VycmVudFBhZ2VJbmRleGZkFgJmD2QWAgIBD2QWDGYPDxYCHwEFBTAwMjEgZGQCAQ8PFgIfAQUEMDIyIGRkAgIPDxYCHwEFITE3MDUgQkFLRVIgU1QgICAgICAgICAgICAgICAgICAgIGRkAgMPZBYIAgEPDxYCHwEFIURFTUFSLCBEQVZJRCAgICAgICAgICAgICAgICAgICAgIGRkAgMPDxYCHwEFITE3MDUgQkFLRVIgU1QgICAgICAgICAgICAgICAgICAgIGRkAgUPDxYCHwEFIUJBTFRJTU9SRSBNRCAyMTIxNy0xNjAyICAgICAgICAgIGRkAgcPDxYCHwEFISAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRkAgQPZBYCAgEPZBYCAgEPFQEhMTcwNSBCQUtFUiBTVCAgICAgICAgICAgICAgICAgICAgZAIFD2QWAgIBD2QWAgIBDxUBITE3MDUgQkFLRVIgU1QgICAgICAgICAgICAgICAgICAgIGQCBg9kFgQCDQ9kFgJmD2QWAmYPZBYCZg8PFgIfAmhkZAIVD2QWAgIBDw8WAh8BBS9QYXkgT25saW5lIHdpdGggQ3JlZGl0IENhcmQgb3IgQ2hlY2tpbmcgQWNjb3VudGRkAgcPZBYCAgcPZBYCAgEPPCsACwBkAggPDxYCHwJoZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgIFHmN0bDAwJGN0bDAwJGltZ0J0bkdvb2dsZVNlYXJjaAUUY3RsMDAkY3RsMDAkUmFkTWVudTGVJdC2P+UeVXl5cdDYZzQRTCbPRg==',
    formdict['__VIEWSTATEGENERATOR'] = 'AE2FC7FE'
    formdict['__EVENTARGUMENT'] = ''
    formdict['ctl00_ctl00_RadMenu1_ClientState'] = ''
    formdict['ctl00$ctl00$rootMasterContent$LocalContentPlaceHolder$hdnDdyear'] = '0'
    formdict['ctl00$ctl00$rootMasterContent$LocalContentPlaceHolder$hdnSYear'] = '2016'
    formdict['ctl00$ctl00$rootMasterContent$LocalContentPlaceHolder$hdnYear'] = '2016'
    formdict['ctl00$ctl00$txtGoogleCustomSearch'] = 'Search Unavailable'
    formdict['ctl00$ctl00$rootMasterContent$LocalContentPlaceHolder$hdnOwner'] = ''
    formdict['ctl00$ctl00$rootMasterContent$LocalContentPlaceHolder$hdnSOwner'] = ''
    
    
    # Site requires only specific fields are filled, e.g., if block and lot are available, clear the Address field
    if block != '' and lot != '':
        formdict['ctl00$ctl00$rootMasterContent$LocalContentPlaceHolder$hdnBlock'] = block
        formdict['ctl00$ctl00$rootMasterContent$LocalContentPlaceHolder$hdnLot'] = lot
        formdict['ctl00$ctl00$rootMasterContent$LocalContentPlaceHolder$hdnAddress'] = ''
    elif homeAddress != '':
        formdict['ctl00$ctl00$rootMasterContent$LocalContentPlaceHolder$hdnAddress'] = homeAddress
        formdict['ctl00$ctl00$rootMasterContent$LocalContentPlaceHolder$hdnBlock'] = ''
        formdict['ctl00$ctl00$rootMasterContent$LocalContentPlaceHolder$hdnLot'] = ''
    
    # hdn and hdnS terms should match
    formdict['ctl00$ctl00$rootMasterContent$LocalContentPlaceHolder$hdnSBlock'] = formdict['ctl00$ctl00$rootMasterContent$LocalContentPlaceHolder$hdnBlock']
    formdict['ctl00$ctl00$rootMasterContent$LocalContentPlaceHolder$hdnSLot'] = formdict['ctl00$ctl00$rootMasterContent$LocalContentPlaceHolder$hdnLot']
    formdict['ctl00$ctl00$rootMasterContent$LocalContentPlaceHolder$hdnSAddress'] = formdict['ctl00$ctl00$rootMasterContent$LocalContentPlaceHolder$hdnAddress']
    
    
    session = Session()
    
    # HEAD requests ask for *just* the headers, which is all you need to grab the
    # session cookie
    session.head('http://cityservices.baltimorecity.gov/realproperty')
    
    response = session.post('http://cityservices.baltimorecity.gov/realproperty/default.aspx',
        data = formdict
    )
    
    # Output rendered HTML page to file in current directory
    #with open('propinfo.html','wb') as f:
    #	f.write(response.text.encode('utf-8'))	
            
    return response.text.encode('utf-8')
	
			
@app.route("/")
def hello():
    return '<html><head><h1>Tax info listings</h3></head><body><a href="/tax/"><h2>tax/</h2></a><a href="/sdat/"><h2>sdat/</h2><a href="https://github.com/geoffreyn/propertytaxinfo.git"><img style="position: absolute; top: 0; right: 0; border: 0;" src="https://camo.githubusercontent.com/a6677b08c955af8400f44c6298f40e7d19cc5b2d/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f677261795f3664366436642e706e67" alt="Fork me on GitHub" data-canonical-src="https://s3.amazonaws.com/github/ribbons/forkme_left_gray_6d6d6d.png"></a></body></html>'

if __name__ == "__main__":
    #app.debug = True
    app.run()
