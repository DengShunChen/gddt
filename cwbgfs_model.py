cwbgfs_model_dict={ \
'GG' : [319,960,480], \
'GH' : [511,1536,768], \
'GJ' : [639,2576,1280] \
}
'''
cwbgfs_model_dict={'model flag' : [jcap,nlon,nlat]}
'''

cwbgfs_level_dict={ \
'SSL' : 'Sea Level', \
'W00' : 'Sea Surface', \
'010' : '10 hPa',  \
'020' : '20 hPa',  \
'030' : '30 hPa', \
'050' : '50 hPa', \
'070' : '70 hPa', \
'100' : '100 hPa', \
'150' : '150 hPa', \
'200' : '200 hPa', \
'250' : '250 hPa', \
'300' : '300 hPa', \
'350' : '350 hPa', \
'400' : '400 hPa', \
'450' : '450 hPa', \
'500' : '500 hPa', \
'550' : '550 hPa', \
'600' : '600 hPa', \
'650' : '650 hPa', \
'700' : '700 hPa', \
'750' : '750 hPa', \
'800' : '800 hPa', \
'850' : '850 hPa', \
'900' : '900 hPa', \
'925' : '925 hPa', \
'950' : '950 hPa', \
'975' : '975 hPa', \
'H00' : '1000 hPa', \
'B00' : 'Surface', \
'B02' : '2 meters', \
'B10' : '10 meters', \
'M01' : 'sigma level 1', \
'M02' : 'sigma level 2', \
'M03' : 'sigma level 3', \
'M04' : 'sigma level 4', \
'M05' : 'sigma level 5', \
'M06' : 'sigma level 6', \
'M07' : 'sigma level 7', \
'M08' : 'sigma level 8', \
'M09' : 'sigma level 9', \
'M10' : 'sigma level 10', \
'M11' : 'sigma level 11', \
'M12' : 'sigma level 12', \
'M13' : 'sigma level 13', \
'M14' : 'sigma level 14', \
'M15' : 'sigma level 15', \
'M16' : 'sigma level 16', \
'M17' : 'sigma level 17', \
'M18' : 'sigma level 18', \
'M19' : 'sigma level 19', \
'M20' : 'sigma level 20', \
'M21' : 'sigma level 21', \
'M22' : 'sigma level 22', \
'M23' : 'sigma level 23', \
'M24' : 'sigma level 24', \
'M25' : 'sigma level 25', \
'M26' : 'sigma level 26', \
'M27' : 'sigma level 27', \
'M28' : 'sigma level 28', \
'M29' : 'sigma level 29', \
'M30' : 'sigma level 30', \
'M31' : 'sigma level 31', \
'M32' : 'sigma level 32', \
'M33' : 'sigma level 33', \
'M34' : 'sigma level 34', \
'M35' : 'sigma level 35', \
'M36' : 'sigma level 36', \
'M37' : 'sigma level 37', \
'M38' : 'sigma level 38', \
'M39' : 'sigma level 39', \
'M40' : 'sigma level 40', \
'M41' : 'sigma level 41', \
'M42' : 'sigma level 42', \
'M43' : 'sigma level 43', \
'M44' : 'sigma level 44', \
'M45' : 'sigma level 45', \
'M46' : 'sigma level 46', \
'M47' : 'sigma level 47', \
'M48' : 'sigma level 48', \
'M49' : 'sigma level 49', \
'M50' : 'sigma level 50', \
'M51' : 'sigma level 51', \
'M52' : 'sigma level 52', \
'M53' : 'sigma level 53', \
'M54' : 'sigma level 54', \
'M55' : 'sigma level 55', \
'M56' : 'sigma level 56', \
'M57' : 'sigma level 57', \
'M58' : 'sigma level 58', \
'M59' : 'sigma level 59', \
'M60' : 'sigma level 60', \
'M61' : 'sigma level 61', \
'M62' : 'sigma level 62', \
'M63' : 'sigma level 63', \
'M64' : 'sigma level 64', \
'M65' : 'sigma level 65', \
'M66' : 'sigma level 66', \
'M67' : 'sigma level 67', \
'M68' : 'sigma level 68', \
'M69' : 'sigma level 69', \
'M70' : 'sigma level 70', \
'M71' : 'sigma level 71', \
'M72' : 'sigma level 72' \
}
'''
cwbgfs_level_dict{'dms levs' : 'name'
'''

cwbgfs_variable_dict={ \
'000' : 'Geopotential Height(m)', \
'010' : 'Pressure (hPa)', \
'100' : 'Temperature (K)', \
'200' : 'U-wind (m/s)', \
'210' : 'V-wind (m/s)', \
'220' : 'Omega Veritical Wind (hPa/h)', \
'230' : 'Divergence (1/s)', \
'500' : 'Specific Humidity (kg/kg)', \
'510' : 'Relative Humidity (%)', \
'550' : 'Cloud Liquid Water mixing ratio (kg/kg)', \
'560' : 'Ozone mixing ratio (kg/kg)' \
}
'''
cwbgfs_variable_dict{'dms var' : 'name'}
'''

cwbgfs_dmsvar_dict={ \
'Geopotential height' : '000', \
'Temperature'         : '100', \
'U component of wind' : '200', \
'V component of wind' : '210', \
'Omega'               : '220', \
'Specific humidity'   : '500', \
'Relative humidity'   : '510', \
'Cloud liquid water mixing ratio' : '550', \
'Ozone mixing ratio'  : '560', \
'Sea Surface Temperature' : '100', \
'Sea Level Pressure'  : '010' \
}

cwbgfs_dmslev_dict={ \
'Sea Surface Temperature' : 'W00', \
'Sea Level Pressure'  : 'SSL' \
}
