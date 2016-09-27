<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">

    <xsl:text disable-output-escaping="yes">&lt;!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" http:"//www.w3.org/TR/xhtml/DTD/xhtml1-strict.dtd"&gt;</xsl:text>

    <html xmlns = "http://www.w3.org/1999/xhtml">
		<head>
			<title>Site References</title>
			<link href="site.css" rel="stylesheet" type="text/css" />
		</head>
		<body>

            <xsl:variable name="id_boxes" select="//box[@id]"/>
			<xsl:variable name="ref_boxes" select="//box[@ref]"/>

			<xsl:variable name="path_items" select="//content[@path]"/>
			<xsl:variable name="zid_items" select="//*[@zid]"/>

            <h1>Site References</h1>

            <div class="section">
			    <h2>Box Ids</h2>
				<xsl:if test="count($id_boxes)=0"><em>None</em></xsl:if>
			    <xsl:for-each select="$id_boxes">
				    <xsl:sort select="@id"/>
					<div><xsl:value-of select="@id"/></div>
				</xsl:for-each>

			    <h2>Box References</h2>
				<xsl:if test="count($ref_boxes)=0"><em>None</em></xsl:if>
			    <xsl:for-each select="$ref_boxes">
				    <xsl:sort select="@ref"/>
					<div><xsl:value-of select="@ref"/></div>
				</xsl:for-each>
			</div>


            <div class="section">
                <h2>Paths</h2>
				<xsl:if test="count($zid_items)=0"><em>None</em></xsl:if>
				<xsl:for-each select="$zid_items">
				    <xsl:for-each select="ancestor-or-self::*[@zid]">
					    <xsl:value-of select="@zid"/>
						<xsl:text>/</xsl:text>
					</xsl:for-each>
					<br/>
				</xsl:for-each>

			    <h2>Path References</h2>
				<xsl:if test="count($path_items)=0"><em>None</em></xsl:if>
				<xsl:for-each select="$path_items">
				    <xsl:sort select="@path"/>
					<div><xsl:value-of select="@path"/></div>
				</xsl:for-each>
			</div>
            
			<br/>
		</body>
	</html>
</xsl:template>



</xsl:stylesheet>





<!-- Stylus Studio meta-information - (c)1998-2003 Copyright Sonic Software Corporation. All rights reserved.
<metaInformation>
<scenarios ><scenario default="no" name="King Lear" userelativepaths="yes" externalpreview="no" url="lear.xml" htmlbaseurl="" outputurl="" processortype="internal" commandline="" additionalpath="" additionalclasspath="" postprocessortype="none" postprocesscommandline="" postprocessadditionalpath="" postprocessgeneratedext=""/><scenario default="yes" name="Site (site1.xml)" userelativepaths="yes" externalpreview="no" url="site1.xml" htmlbaseurl="..\project4" outputurl="" processortype="internal" commandline="" additionalpath="" additionalclasspath="" postprocessortype="none" postprocesscommandline="" postprocessadditionalpath="" postprocessgeneratedext=""/><scenario default="no" name="Site (site2.xml)" userelativepaths="yes" externalpreview="no" url="site2.xml" htmlbaseurl="..\project4" outputurl="" processortype="internal" commandline="" additionalpath="" additionalclasspath="" postprocessortype="none" postprocesscommandline="" postprocessadditionalpath="" postprocessgeneratedext=""/><scenario default="no" name="Site (site3.xml)" userelativepaths="yes" externalpreview="no" url="site3.xml" htmlbaseurl="..\project4" outputurl="" processortype="internal" commandline="" additionalpath="" additionalclasspath="" postprocessortype="none" postprocesscommandline="" postprocessadditionalpath="" postprocessgeneratedext=""/></scenarios><MapperInfo srcSchemaPath="" srcSchemaRoot="" srcSchemaPathIsRelative="yes" srcSchemaInterpretAsXML="no" destSchemaPath="" destSchemaRoot="" destSchemaPathIsRelative="yes" destSchemaInterpretAsXML="no"/>
</metaInformation>
-->