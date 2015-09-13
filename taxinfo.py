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
        
        
    # format standard request header, suggesting we're accessing the page from a browser
    header = {
            'Host': 'sdat.dat.maryland.gov',
            'Origin': 'http://sdat.dat.maryland.gov',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:40.0) Gecko/20100101 Firefox/40.0.2 Waterfox/40.0.2',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'DNT': '1',
            'Referer': 'http://sdat.dat.maryland.gov/RealProperty/Pages/default.aspx',
            'Cookie': '_gat=1; ASP.NET_SessionId=ridcsennnwadebhb4gzigmkn; _ga=GA1.2.292490867.1442124144; _ga=GA1.1.292490867.1442124144',
            'Connection': 'keep-alive',
            'X-MicrosoftAjax': 'Delta=true',
            'X-Requested-With': 'XMLHttpRequest'
        }

    session = Session()


    # HEAD requests ask for *just* the headers, which is all you need to grab the
    # session cookie
    session.head('http://sdat.dat.maryland.gov/RealProperty/Pages')

    response = session.post(
        url='http://sdat.dat.maryland.gov/RealProperty/Pages/default.aspx',
        data = formdict,
        headers = header
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
    formdict = {}

    formdict['__EVENTTARGET'] = 'ctl00$ctl00$rootMasterContent$LocalContentPlaceHolder$DataGrid1$ctl02$lnkBtnSelect'
    formdict['__VIEWSTATE'] = '/wEPDwULLTEyMDI3MzkzODIPFgIeBVllYXJzFQQEMjAxNgQyMDE1BDIwMTQEMjAxMxYCZg9kFgJmD2QWBGYPZBYEAgIPFgIeBFRleHRlZAIFDxYCHgdWaXNpYmxlZxYCZg8WAh8BZWQCAQ9kFgoCAQ8PFgIeCEltYWdlVXJsBVZodHRwOi8vY2l0eXNlcnZpY2VzLmJhbHRpbW9yZWNpdHkuZ292L3JlbW90ZW1hc3RlcnYzL2ltYWdlcy9pbnRlcm5ldC9pY29ucy9sb2FkaW5nLmdpZmRkAgQPFgIfAmdkAgYPFgIfAmcWAgIBDxYCHwEFDVJlYWwgUHJvcGVydHlkAgcPZBYIAgEPZBYCAgEPZBYEZg8PFgYfAQUSU2VhcmNoIFVuYXZhaWxhYmxlHgdUb29sVGlwBThTZWFyY2ggaXMgY3VycmVudGx5IHVuYXZhaWxhYmxlLCBwbGVhc2UgdHJ5IGFnYWluIGxhdGVyLh4IUmVhZE9ubHlnFgQeB29uZm9jdXMFMWlmKHRoaXMudmFsdWU9PSdLZXl3b3JkIG9yIFNlYXJjaCcpdGhpcy52YWx1ZT0nJzseBm9uYmx1cgUxaWYodGhpcy52YWx1ZT09JycpdGhpcy52YWx1ZT0nS2V5d29yZCBvciBTZWFyY2gnO2QCAQ8PFgIeB0VuYWJsZWRoFgIeB29uY2xpY2sFaGlmKGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdjdGwwMF9jdGwwMF90eHRHb29nbGVDdXN0b21TZWFyY2gnKS52YWx1ZT09J0tleXdvcmQgb3IgU2VhcmNoJylyZXR1cm4gZmFsc2U7ZAICD2QWBAIBDxYCHwEFDEZpbmFuY2UgTWVudWQCAw8UKwACFCsAAg8WBh4LXyFEYXRhQm91bmRnHhdFbmFibGVBamF4U2tpblJlbmRlcmluZ2geDERhdGFTb3VyY2VJRAUSU2l0ZU1hcERhdGFTb3VyY2UxZA8UKwATFCsAAg8WCB8BBQRIb21lHgtOYXZpZ2F0ZVVybAU5aHR0cDovL3d3dy5iYWx0aW1vcmVjaXR5Lmdvdi9nb3Zlcm5tZW50L2ZpbmFuY2UvaW5kZXgucGhwHgVWYWx1ZQUESG9tZR8EBQRIb21lZGQUKwACDxYIHwEFFEFjY291bnRpbmcgJiBQYXlyb2xsHw0FO2h0dHA6Ly93d3cuYmFsdGltb3JlY2l0eS5nb3YvZ292ZXJubWVudC9maW5hbmNlL2FjY291bnQucGhwHw4FFEFjY291bnRpbmcgJiBQYXlyb2xsHwQFFEFjY291bnRpbmcgJiBQYXlyb2xsZGQUKwACDxYIHwEFHEJ1ZGdldCAmIE1hbmFnZW1lbnQgUmVzZWFyY2gfDQU4aHR0cDovL3d3dy5iYWx0aW1vcmVjaXR5Lmdvdi9nb3Zlcm5tZW50L2ZpbmFuY2UvYmJtci5waHAfDgUcQnVkZ2V0ICYgTWFuYWdlbWVudCBSZXNlYXJjaB8EBRxCdWRnZXQgJiBNYW5hZ2VtZW50IFJlc2VhcmNoZGQUKwACDxYIHwEFCVB1cmNoYXNlcx8NBT1odHRwOi8vd3d3LmJhbHRpbW9yZWNpdHkuZ292L2dvdmVybm1lbnQvZmluYW5jZS9wdXJjaGFzZXMucGhwHw4FCVB1cmNoYXNlcx8EBQlQdXJjaGFzZXNkZBQrAAIPFggfAQUPUmlzayBNYW5hZ2VtZW50Hw0FPGh0dHA6Ly93d3cuYmFsdGltb3JlY2l0eS5nb3YvZ292ZXJubWVudC9maW5hbmNlL3Jpc2ttZ210LnBocB8OBQ9SaXNrIE1hbmFnZW1lbnQfBAUPUmlzayBNYW5hZ2VtZW50ZGQUKwACDxYIHwEFE1RyZWFzdXJ5IE1hbmFnZW1lbnQfDQU8aHR0cDovL3d3dy5iYWx0aW1vcmVjaXR5Lmdvdi9nb3Zlcm5tZW50L2ZpbmFuY2UvdHJlYXN1cnkucGhwHw4FE1RyZWFzdXJ5IE1hbmFnZW1lbnQfBAUTVHJlYXN1cnkgTWFuYWdlbWVudGRkFCsAAg8WCB8BBRNSZXZlbnVlIENvbGxlY3Rpb25zHw0FO2h0dHA6Ly93d3cuYmFsdGltb3JlY2l0eS5nb3YvZ292ZXJubWVudC9maW5hbmNlL3JldmVudWUucGhwHw4FE1JldmVudWUgQ29sbGVjdGlvbnMfBAUTUmV2ZW51ZSBDb2xsZWN0aW9uc2RkFCsAAg8WCB8BBRNEb2N1bWVudHMgJiBSZXBvcnRzHw0FOGh0dHA6Ly93d3cuYmFsdGltb3JlY2l0eS5nb3YvZ292ZXJubWVudC9maW5hbmNlL2RvY3MucGhwHw4FE0RvY3VtZW50cyAmIFJlcG9ydHMfBAUTRG9jdW1lbnRzICYgUmVwb3J0c2RkFCsAAg8WCB8BBQ9PbmxpbmUgUGF5bWVudHMfDQUtaHR0cDovL2NpdHlzZXJ2aWNlcy5iYWx0aW1vcmVjaXR5Lmdvdi9wYXlzeXMvHw4FD09ubGluZSBQYXltZW50cx8EBQ9PbmxpbmUgUGF5bWVudHNkZBQrAAIPFggfAQUTPGgyPkZBUSAvIEhlbHA8L2gyPh8NBQ8vUmVhbFByb3BlcnR5LyMfDgUTPGgyPkZBUSAvIEhlbHA8L2gyPh8EZWRkFCsAAg8WCB8BBQ1UYXggU2FsZSBGQVFzHw0FG2h0dHA6Ly93d3cuYmlkYmFsdGltb3JlLmNvbR8OBQ1UYXggU2FsZSBGQVFzHwQFDVRheCBTYWxlIEZBUXNkZBQrAAIPFggfAQURUGFya2luZyBGaW5lcyBGQVEfDQVBaHR0cDovL3d3dy5iYWx0aW1vcmVjaXR5Lmdvdi9hbnN3ZXJzL2luZGV4LnBocD9hY3Rpb249c2hvdyZjYXQ9MTAfDgURUGFya2luZyBGaW5lcyBGQVEfBAURUGFya2luZyBGaW5lcyBGQVFkZBQrAAIPFggfAQURUmVhbCBQcm9wZXJ0eSBGQVEfDQVBaHR0cDovL3d3dy5iYWx0aW1vcmVjaXR5Lmdvdi9hbnN3ZXJzL2luZGV4LnBocD9hY3Rpb249c2hvdyZjYXQ9MTIfDgURUmVhbCBQcm9wZXJ0eSBGQVEfBAURUmVhbCBQcm9wZXJ0eSBGQVFkZBQrAAIPFggfAQUVUGFya2luZyBGaW5lcyBMaXN0aW5nHw0Fa2h0dHA6Ly93d3cuYmFsdGltb3JlY2l0eS5nb3YvZ292ZXJubWVudC90cmFuc3BvcnRhdGlvbi9kb3dubG9hZHMvMTIwNy8xMjE5MDcgUGFya2luZyBGaW5lcyBMaXN0aW5nIDIwMDcucGRmHw4FFVBhcmtpbmcgRmluZXMgTGlzdGluZx8EBRVQYXJraW5nIEZpbmVzIExpc3RpbmdkZBQrAAIPFggfAQUYQXZvaWRpbmcgUGFya2luZyBUaWNrZXRzHw0FaGh0dHA6Ly93d3cuYmFsdGltb3JlY2l0eS5nb3YvZ292ZXJubWVudC90cmFuc3BvcnRhdGlvbi9kb3dubG9hZHMvMTIwNy8xMjE5MDcgUGFya2luZyBUaWNrZXQgQnJvY2h1cmUucGRmHw4FGEF2b2lkaW5nIFBhcmtpbmcgVGlja2V0cx8EBRhBdm9pZGluZyBQYXJraW5nIFRpY2tldHNkZBQrAAIPFggfAQURVHJhbnNmZXIgVGF4IFVuaXQfDQVBaHR0cDovL3d3dy5iYWx0aW1vcmVjaXR5Lmdvdi9hbnN3ZXJzL2luZGV4LnBocD9hY3Rpb249c2hvdyZjYXQ9MTEfDgURVHJhbnNmZXIgVGF4IFVuaXQfBAURVHJhbnNmZXIgVGF4IFVuaXRkZBQrAAIPFggfAQUKTGllbnMgVW5pdB8NBT1odHRwOi8vd3d3LmJhbHRpbW9yZWNpdHkuZ292L2dvdmVybm1lbnQvZmluYW5jZS9mYXF0bGllbnMucGhwHw4FCkxpZW5zIFVuaXQfBAUKTGllbnMgVW5pdGRkFCsAAg8WCB8BBRdMaWVuIENlcnRpZmljYXRlIFBvbGljeR8NBV9odHRwOi8vd3d3LmJhbHRpbW9yZWNpdHkuZ292L2dvdmVybm1lbnQvZmluYW5jZS9pbWFnZXMvTGllbiBDZXJ0aWZpY2F0ZSBwb2xpY3kgXzJfIE9jdCAyMDA4LnBkZh8OBRdMaWVuIENlcnRpZmljYXRlIFBvbGljeR8EBRdMaWVuIENlcnRpZmljYXRlIFBvbGljeWRkFCsAAg8WCB8BBQhDb250YWN0cx8NZR8OBQhDb250YWN0cx8EZWRkDxQrARNmZmZmZmZmZmZmZmZmZmZmZmZmFgEFc1RlbGVyaWsuV2ViLlVJLlJhZE1lbnVJdGVtLCBUZWxlcmlrLldlYi5VSSwgVmVyc2lvbj0yMDA4LjIuODI2LjIwLCBDdWx0dXJlPW5ldXRyYWwsIFB1YmxpY0tleVRva2VuPTEyMWZhZTc4MTY1YmEzZDRkFiZmDw8WCB8BBQRIb21lHw0FOWh0dHA6Ly93d3cuYmFsdGltb3JlY2l0eS5nb3YvZ292ZXJubWVudC9maW5hbmNlL2luZGV4LnBocB8OBQRIb21lHwQFBEhvbWVkZAIBDw8WCB8BBRRBY2NvdW50aW5nICYgUGF5cm9sbB8NBTtodHRwOi8vd3d3LmJhbHRpbW9yZWNpdHkuZ292L2dvdmVybm1lbnQvZmluYW5jZS9hY2NvdW50LnBocB8OBRRBY2NvdW50aW5nICYgUGF5cm9sbB8EBRRBY2NvdW50aW5nICYgUGF5cm9sbGRkAgIPDxYIHwEFHEJ1ZGdldCAmIE1hbmFnZW1lbnQgUmVzZWFyY2gfDQU4aHR0cDovL3d3dy5iYWx0aW1vcmVjaXR5Lmdvdi9nb3Zlcm5tZW50L2ZpbmFuY2UvYmJtci5waHAfDgUcQnVkZ2V0ICYgTWFuYWdlbWVudCBSZXNlYXJjaB8EBRxCdWRnZXQgJiBNYW5hZ2VtZW50IFJlc2VhcmNoZGQCAw8PFggfAQUJUHVyY2hhc2VzHw0FPWh0dHA6Ly93d3cuYmFsdGltb3JlY2l0eS5nb3YvZ292ZXJubWVudC9maW5hbmNlL3B1cmNoYXNlcy5waHAfDgUJUHVyY2hhc2VzHwQFCVB1cmNoYXNlc2RkAgQPDxYIHwEFD1Jpc2sgTWFuYWdlbWVudB8NBTxodHRwOi8vd3d3LmJhbHRpbW9yZWNpdHkuZ292L2dvdmVybm1lbnQvZmluYW5jZS9yaXNrbWdtdC5waHAfDgUPUmlzayBNYW5hZ2VtZW50HwQFD1Jpc2sgTWFuYWdlbWVudGRkAgUPDxYIHwEFE1RyZWFzdXJ5IE1hbmFnZW1lbnQfDQU8aHR0cDovL3d3dy5iYWx0aW1vcmVjaXR5Lmdvdi9nb3Zlcm5tZW50L2ZpbmFuY2UvdHJlYXN1cnkucGhwHw4FE1RyZWFzdXJ5IE1hbmFnZW1lbnQfBAUTVHJlYXN1cnkgTWFuYWdlbWVudGRkAgYPDxYIHwEFE1JldmVudWUgQ29sbGVjdGlvbnMfDQU7aHR0cDovL3d3dy5iYWx0aW1vcmVjaXR5Lmdvdi9nb3Zlcm5tZW50L2ZpbmFuY2UvcmV2ZW51ZS5waHAfDgUTUmV2ZW51ZSBDb2xsZWN0aW9ucx8EBRNSZXZlbnVlIENvbGxlY3Rpb25zZGQCBw8PFggfAQUTRG9jdW1lbnRzICYgUmVwb3J0cx8NBThodHRwOi8vd3d3LmJhbHRpbW9yZWNpdHkuZ292L2dvdmVybm1lbnQvZmluYW5jZS9kb2NzLnBocB8OBRNEb2N1bWVudHMgJiBSZXBvcnRzHwQFE0RvY3VtZW50cyAmIFJlcG9ydHNkZAIIDw8WCB8BBQ9PbmxpbmUgUGF5bWVudHMfDQUtaHR0cDovL2NpdHlzZXJ2aWNlcy5iYWx0aW1vcmVjaXR5Lmdvdi9wYXlzeXMvHw4FD09ubGluZSBQYXltZW50cx8EBQ9PbmxpbmUgUGF5bWVudHNkZAIJDw8WCB8BBRM8aDI+RkFRIC8gSGVscDwvaDI+Hw0FDy9SZWFsUHJvcGVydHkvIx8OBRM8aDI+RkFRIC8gSGVscDwvaDI+HwRlZGQCCg8PFggfAQUNVGF4IFNhbGUgRkFRcx8NBRtodHRwOi8vd3d3LmJpZGJhbHRpbW9yZS5jb20fDgUNVGF4IFNhbGUgRkFRcx8EBQ1UYXggU2FsZSBGQVFzZGQCCw8PFggfAQURUGFya2luZyBGaW5lcyBGQVEfDQVBaHR0cDovL3d3dy5iYWx0aW1vcmVjaXR5Lmdvdi9hbnN3ZXJzL2luZGV4LnBocD9hY3Rpb249c2hvdyZjYXQ9MTAfDgURUGFya2luZyBGaW5lcyBGQVEfBAURUGFya2luZyBGaW5lcyBGQVFkZAIMDw8WCB8BBRFSZWFsIFByb3BlcnR5IEZBUR8NBUFodHRwOi8vd3d3LmJhbHRpbW9yZWNpdHkuZ292L2Fuc3dlcnMvaW5kZXgucGhwP2FjdGlvbj1zaG93JmNhdD0xMh8OBRFSZWFsIFByb3BlcnR5IEZBUR8EBRFSZWFsIFByb3BlcnR5IEZBUWRkAg0PDxYIHwEFFVBhcmtpbmcgRmluZXMgTGlzdGluZx8NBWtodHRwOi8vd3d3LmJhbHRpbW9yZWNpdHkuZ292L2dvdmVybm1lbnQvdHJhbnNwb3J0YXRpb24vZG93bmxvYWRzLzEyMDcvMTIxOTA3IFBhcmtpbmcgRmluZXMgTGlzdGluZyAyMDA3LnBkZh8OBRVQYXJraW5nIEZpbmVzIExpc3RpbmcfBAUVUGFya2luZyBGaW5lcyBMaXN0aW5nZGQCDg8PFggfAQUYQXZvaWRpbmcgUGFya2luZyBUaWNrZXRzHw0FaGh0dHA6Ly93d3cuYmFsdGltb3JlY2l0eS5nb3YvZ292ZXJubWVudC90cmFuc3BvcnRhdGlvbi9kb3dubG9hZHMvMTIwNy8xMjE5MDcgUGFya2luZyBUaWNrZXQgQnJvY2h1cmUucGRmHw4FGEF2b2lkaW5nIFBhcmtpbmcgVGlja2V0cx8EBRhBdm9pZGluZyBQYXJraW5nIFRpY2tldHNkZAIPDw8WCB8BBRFUcmFuc2ZlciBUYXggVW5pdB8NBUFodHRwOi8vd3d3LmJhbHRpbW9yZWNpdHkuZ292L2Fuc3dlcnMvaW5kZXgucGhwP2FjdGlvbj1zaG93JmNhdD0xMR8OBRFUcmFuc2ZlciBUYXggVW5pdB8EBRFUcmFuc2ZlciBUYXggVW5pdGRkAhAPDxYIHwEFCkxpZW5zIFVuaXQfDQU9aHR0cDovL3d3dy5iYWx0aW1vcmVjaXR5Lmdvdi9nb3Zlcm5tZW50L2ZpbmFuY2UvZmFxdGxpZW5zLnBocB8OBQpMaWVucyBVbml0HwQFCkxpZW5zIFVuaXRkZAIRDw8WCB8BBRdMaWVuIENlcnRpZmljYXRlIFBvbGljeR8NBV9odHRwOi8vd3d3LmJhbHRpbW9yZWNpdHkuZ292L2dvdmVybm1lbnQvZmluYW5jZS9pbWFnZXMvTGllbiBDZXJ0aWZpY2F0ZSBwb2xpY3kgXzJfIE9jdCAyMDA4LnBkZh8OBRdMaWVuIENlcnRpZmljYXRlIFBvbGljeR8EBRdMaWVuIENlcnRpZmljYXRlIFBvbGljeWRkAhIPDxYIHwEFCENvbnRhY3RzHw1lHw4FCENvbnRhY3RzHwRlZGQCBQ8WAh8BBRE8aDI+Q09OVEFDVFM8L2gyPmQCBg8WAh8BBasDPGRpdiBzdHlsZT0ncGFkZGluZzoxMHB4Oyc+PGEgaHJlZj0nbWFpbHRvOkJhbHRpbW9yZUNpdHlDb2xsZWN0aW9uc0BiYWx0aW1vcmVjaXR5Lmdvdic+PHN0cm9uZz5SZXZlbnVlIENvbGxlY3Rpb25zPC9zdHJvbmc+PC9hPjxici8+MjAwIEhvbGxpZGF5IFN0LiwgUm9vbSA3PGJyLz48YnIvPjxhIGhyZWY9J2h0dHA6Ly93d3cuYmFsdGltb3JlY2l0eS5nb3YvZ292ZXJubWVudC9maW5hbmNlL3JldmVudWUucGhwI2NvbnRhY3RzJz48c3Ryb25nPkFsbCAgQ29udGFjdCBOdW1iZXJzPC9zdHJvbmc+PC9hPjxici8+PGJyIC8+IDxici8+PGgxPkFkbWluaXN0cmF0aW9uPC9oMT4gPGJyLz48c3Ryb25nPiBIZW5yeSBSYXltb25kICA8YnIgLz4gPC9zdHJvbmc+PGVtPkNoaWVmPC9lbT48YnIgLz5CdXJlYXUgb2YgUmV2ZW51ZSBDb2xsZWN0aW9uczwvZGl2PmQCCQ9kFgICAQ9kFhACAQ8WAh4EaHJlZgU2aHR0cDovL2NpdHlzZXJ2aWNlcy5iYWx0aW1vcmVjaXR5Lmdvdi9TcGVjaWFsQmVuZWZpdHMvZAICDw8WBB8BBW1UaGUgRVhFQ1VURSBwZXJtaXNzaW9uIHdhcyBkZW5pZWQgb24gdGhlIG9iamVjdCAnQWRkTG9nRW50cnknLCBkYXRhYmFzZSAnRmluYW5jZV9SZWFsUHJvcGVydHknLCBzY2hlbWEgJ2RibycuHwJoZGQCAw8PFgIfAmhkFgZmDxBkDxYEZgIBAgICAxYEEAUJMjAxNS8yMDE2BQQyMDE2ZxAFCTIwMTQvMjAxNQUEMjAxNWcQBQkyMDEzLzIwMTQFBDIwMTRnEAUJMjAxMi8yMDEzBQQyMDEzZxYBZmQCBA8PFgIfAQUPMjkxOSBzYWludCBwYXVsZGQCBg8PFgIfAmhkZAIEDw8WAh8CaGQWAgIBDxYCHwEFgAk8b2w+PGxpPlRoaXMgcGFnZSBpcyBmb3IgUmVhbCBQcm9wZXJ0eSB0YXhlcy4gIFVzZSB0aGlzIGxpbmsgZm9yIDxhIGhyZWY9Jy9TcGVjaWFsQmVuZWZpdHMvJz5TcGVjaWFsIEJlbmVmaXQgRGlzdHJpY3QgU3VyY2hhcmdlczwvYT4uIA0KPGxpPklmIHlvdSBrbm93IHRoZSBCbG9jayAmIExvdCwgZW50ZXIgb25seSB0aGUgYmxvY2sgJiBsb3QuIA0KPGxpPklmIHlvdSBhcmUgc2VhcmNoaW5nIGJ5IHByb3BlcnR5IGFkZHJlc3Mgb3Igb3duZXIgbmFtZSwgeW91IG1heSBlbnRlciBhbnkgcG9ydGlvbiBvZiBlaXRoZXIgb3IgYm90aCBvZiB0aG9zZSBmaWVsZHMuICBXaGVuIHlvdSBlbnRlciBkYXRhIGluIGEgc2VhcmNoIGZpZWxkLCB0aGUgZGF0YSB5b3UgZW50ZXJlZCBpcyBsb29rZWQgZm9yIGFueXdoZXJlIHdpdGhpbiB0aGF0IGZpZWxkLiBGb3IgZXhhbXBsZSwgaWYgeW91IGVudGVyIEJsdWUgaW4gdGhlIEFkZHJlc3MgZmllbGQsIHlvdSB3aWxsIGdldCByZXN1bHRzIGluY2x1ZGluZyBCbHVlYmVycnksIEJsdWVib25uZXQsIFRydWVCbHVlLCBldGMuIA0KPGxpPkRpcmVjdGlvbnMgc3VjaCBhcyBOb3J0aCwgU291dGgsIEVhc3QsIFdlc3Qgc2hvdWxkIGJlIGVudGVyZWQgYXMgTixTLEUsVyB3aXRoIG5vIHBlcmlvZC4gDQo8bGk+SWYgeW91ciBzZWFyY2ggZmFpbHMsIHJldHJ5IHdpdGggbGVzcyBpbmZvcm1hdGlvbiBzdWNoIGFzLCBGaXJzdCBTZWFyY2g6IE93bmVyPVJvc2VuYmxhdHQsIHJlc3VsdHM9MCBTZWNvbmQgU2VhcmNoOiBPd25lcj1Sb3NlbiByZXN1bHRzPTEyNCANCjxsaT5MZWF2ZSBvZmYgYWxsIHN0cmVldCBzdWZmaXhlcyBzdWNoIGFzIFN0LixXYXksIFJvYWQgZXRjLiANCjxsaT5XaGVuIHNlYXJjaGluZyBieSBuYW1lLCBlbnRlciBpbiBMYXN0TmFtZSwgRmlyc3ROYW1lIGZvcm1hdC4gDQo8bGk+SWYgYWxsIHlvdXIgc2VhcmNoZXMgYXJlIHVuc3VjY2Vzc2Z1bCwgcGxlYXNlIGNvbnRhY3QgdGhlIERlcHQuIG9mIEZpbmFuY2UgYXQgNDEwLTM5Ni0zOTg3DQo8bGk+PHN0cm9uZz5SZXR1cm5lZCBzZWFyY2ggcmVzdWx0cyBhcmUgbGltaXRlZCB0byA1MCByZWNvcmRzLiBJZiB5b3UgcmVhY2ggdGhpcyBsaW1pdCwgcGxlYXNlIHJlZmluZSB5b3VyIHNlYXJjaCBjcml0ZXJpYS48c3Ryb25nPg0KPC9vbD5kAgUPDxYCHwJnZBYKAgEPDxYEHwJnHwEFNjxiPkNyaXRlcmlhIFVzZWQ6PC9iPlllYXI9MjAxNiBBZGRyZXNzPTI5MTkgc2FpbnQgcGF1bGRkAgMPDxYIHglGb3JlQ29sb3IKkAEfAQUWPGI+UmVjb3JkcyBmb3VuZDo8L2I+MR8CZx4EXyFTQgIEZGQCBQ8PFgQfAmcfAQUZPGI+U29ydGVkIEJ5OjwvYj5CbG9ja0xvdGRkAgcPDxYCHwJnZGQCCQ88KwALAQAPFgweC18hSXRlbUNvdW50AgEeCERhdGFLZXlzFgEFCTM4NTIgMDMyIB4MRGF0YUtleUZpZWxkBQhibG9ja2xvdB4JUGFnZUNvdW50AgEeFV8hRGF0YVNvdXJjZUl0ZW1Db3VudAIBHhBDdXJyZW50UGFnZUluZGV4ZmQWAmYPZBYCAgEPZBYMZg8PFgIfAQUFMzg1MiBkZAIBDw8WAh8BBQQwMzIgZGQCAg8PFgIfAQUhMjkxOSBTQUlOVCBQQVVMIFNUICAgICAgICAgICAgICAgZGQCAw9kFggCAQ8PFgIfAQUhSElORUdBUkRORVIsIENIRVNMSUUgSCAgICAgICAgICAgZGQCAw8PFgIfAQUhSElORUdBUkRORVIsIFRIRUxNQSBQICAgICAgICAgICAgZGQCBQ8PFgIfAQUhSElORUdBUkRORVIsIFdFU0xJRSBKICAgICAgICAgICAgZGQCBw8PFgIfAQUhMTYgRSBMQUtFIEFWRSAgICAgICAgICAgICAgICAgICAgZGQCBA9kFgICAQ9kFgICAQ8VASEyOTE5IFNBSU5UIFBBVUwgU1QgICAgICAgICAgICAgICBkAgUPZBYCAgEPZBYCAgEPFQEhMjkxOSBTQUlOVCBQQVVMIFNUICAgICAgICAgICAgICAgZAIGD2QWBAIND2QWAmYPZBYCZg9kFgJmDw8WAh8CaGRkAhUPZBYCAgEPDxYCHwEFL1BheSBPbmxpbmUgd2l0aCBDcmVkaXQgQ2FyZCBvciBDaGVja2luZyBBY2NvdW50ZGQCBw9kFgICBw9kFgICAQ88KwALAGQCCA8PFgIfAmhkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAgUeY3RsMDAkY3RsMDAkaW1nQnRuR29vZ2xlU2VhcmNoBRRjdGwwMCRjdGwwMCRSYWRNZW51MXDbEEWH2039l2oHCHqw20uQUESS'
    formdict['__VIEWSTATEGENERATOR'] = 'AE2FC7FE'
    formdict['ctl00$ctl00$rootMasterContent$LocalContentPlaceHolder$hdnDdyear'] = '0'
    formdict['ctl00$ctl00$rootMasterContent$LocalContentPlaceHolder$hdnSYear'] = '2016'
    formdict['ctl00$ctl00$rootMasterContent$LocalContentPlaceHolder$hdnYear'] = '2016'
    formdict['ctl00$ctl00$txtGoogleCustomSearch'] = 'Search Unavailable'

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

    # format standard request header, suggesting we're accessing the page from a browser
    header = {
            'Host': 'cityservices.baltimorecity.gov',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:40.0) Gecko/20100101 Firefox/40.0.2 Waterfox/40.0.2',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Referer': 'http://cityservices.baltimorecity.gov/realproperty/default.aspx',
            'Cookie': '_ga=GA1.2.2062381308.1428954099; mp_1d804068e1d3694468823f3c7f74567d_mixpanel=%7B%22distinct_id%22%3A%20%2214cb44d2de3162-01db7f5e997e92-44564136-1fa400-14cb44d2de422a%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D; __cfduid=de1f4fbbc270aa62b4d2bf392f18c8dbb1442023631; ASP.NET_SessionId=vvu4ni450ckn2andelxu4jra; __utma=231819392.2062381308.1428954099.1442080045.1442082439.2; __utmc=231819392; __utmz=231819392.1442080045.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmb=231819392.1.10.1442082439; __utmt=1',
            'Connection': 'keep-alive'
        }

    session = Session()


    # HEAD requests ask for *just* the headers, which is all you need to grab the
    # session cookie
    session.head('http://cityservices.baltimorecity.gov/realproperty')

    response = session.post(
        url='http://cityservices.baltimorecity.gov/realproperty/default.aspx',
        data = formdict,
        headers = header
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
