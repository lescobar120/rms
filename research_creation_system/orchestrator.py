# =============================================================================
# ORCHESTRATOR
# =============================================================================


from typing import List, Dict, Any, Optional, Tuple, Union, Type
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import datetime
import pandas as pd
from pathlib import Path
import os

from .base.template_base import BaseTemplate, BasePublishingConfig, BaseCDEMappingConfig
from .templates.registry import TEMPLATE_REGISTRY

from .document_generation import BloombergReportGenerator, TableStyle
from .document_generation.utils import convert_docx_to_pdf_silently
from .data_models import CompanyInfo, InvestmentRecommendation

from bloomberg_apis.rms_api import (
    initialize_notepublisher_client, 
    initialize_cdeuploader_client,
    initialize_rmsbql_client,
    UserType, CMTY, BBG_USER, NOTE_SECURITY, TAGLIST
)


class ResearchContentOrchestrator:
    """
    Orchestrates research content generation and publishing using template system
    """
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize the orchestrator
        
        Args:
            output_dir: Directory for generated files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize Bloomberg API clients
        self.note_publisher = None
        self.cde_uploader = None
        self.bql_client = None
        
    def _initialize_clients(self):
        """Initialize Bloomberg API clients if not already done"""
        if self.note_publisher is None:
            self.note_publisher = initialize_notepublisher_client()
        if self.cde_uploader is None:
            self.cde_uploader = initialize_cdeuploader_client()
        if self.bql_client is None:
            self.bql_client = initialize_rmsbql_client()
    
    def create_note_tags_and_shareables(self, 
                                      ticker: str,
                                      template: BaseTemplate,
                                      data: Any,
                                      config: BasePublishingConfig) -> Tuple[List, List]:
        """
        Create tags and shareables for note publishing
        
        Args:
            ticker: Primary security ticker
            template: Template instance 
            data: Template data
            config: Publishing configuration
            
        Returns:
            Tuple of (tags_list, shareables_list)
        """
        self._initialize_clients()
        
        # Find primary security
        security = self.note_publisher.find_security(ticker)
        if not security:
            raise ValueError(f"Could not find security: {ticker}")
        
        # Find author
        author = self.note_publisher.find_user(config.analyst_name, UserType.AUTHORS)
        if not author:
            raise ValueError(f"Could not find author: {config.analyst_name}")
        
        # Find taglists
        taglist_entities = []
        for taglist_mapping in config.taglists:
            taglist = self.note_publisher.find_taglist(
                taglist_mapping.taglist_name, 
                taglist_mapping.enum_value
            )
            if not taglist:
                raise ValueError(f"Could not find taglist: {taglist_mapping.taglist_name} - {taglist_mapping.enum_value}")
            taglist_entities.append(taglist)
        
        # Find community
        community = self.note_publisher.find_community(config.community_name)
        if not community:
            raise ValueError(f"Could not find community: {config.community_name}")
        
        tags = [security, author] + taglist_entities
        shareables = [community]
        
        return tags, shareables
    
    def publish_research(self,
                        template_type: Type[BaseTemplate],
                        ticker: str, 
                        data: Any,
                        publishing_config: BasePublishingConfig,
                        cde_config: BaseCDEMappingConfig,
                        note_title: Optional[str] = None,
                        note_body: Optional[str] = None,
                        style_config: Optional[TableStyle] = None,
                        upload_cde: bool = True) -> Dict[str, Any]:
        """
        Complete orchestrated workflow using specified template
        
        Args:
            template_type: Template class to use
            ticker: Primary security ticker
            data: Template-specific data
            publishing_config: Publishing configuration
            cde_config: CDE mapping configuration
            note_title: Custom note title
            note_body: Note body text
            style_config: Document styling
            upload_cde: Whether to upload CDE data
            
        Returns:
            Dictionary with results from each step
        """
        results = {}
        
        try:
            # Initialize template
            template = template_type(style_config)
            template.validate_data(data)
            
            # Step 1: Generate documents
            print(f"Generating {template.template_name} documents...")
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = self.output_dir / f"{template.template_name}_{ticker.replace(' ', '_')}_{timestamp}"
            
            file_paths = template.generate_document(data, str(output_filename))
            results['documents'] = file_paths
            print(f"✓ Documents generated: {list(file_paths.values())}")
            
            # Step 2: Create note tags and shareables
            print("Creating note entities...")
            self._initialize_clients()
            tags, shareables = self.create_note_tags_and_shareables(
                ticker, template, data, publishing_config
            )
            results['entities'] = {
                'tags': [tag.model_dump() for tag in tags],
                'shareables': [shareable.model_dump() for shareable in shareables]
            }
            print("✓ Note entities created")
            
            # Step 3: Publish note
            print("Publishing note to Bloomberg RMS...")
            if note_title is None:
                note_title = f"{data.company_info.name} - {template.template_name.title()} Analysis"
            if note_body is None:
                note_body = f"{template.template_name.title()} analysis for {data.company_info.name}"
            
            # Convert date to timestamp
            as_of_timestamp = int(datetime.datetime.strptime(
                publishing_config.as_of_date, '%Y-%m-%d'
            ).timestamp() * 1000)
            
            # Get attachment paths for the file types this template generates
            attachment_paths = list(file_paths.values())
            
            note_response = self.note_publisher.create_note(
                title=note_title,
                body=note_body,
                as_of_date=as_of_timestamp,
                tags=tags,
                share_with=shareables,
                attachments=attachment_paths
            )
            results['note'] = note_response
            print("✓ Note published successfully")
            
            # Step 4: Upload CDE data (optional)
            if upload_cde:
                print("Uploading CDE data...")
                cde_df = template.prepare_cde_data(data, ticker, publishing_config, cde_config)
                if not cde_df.empty:
                    cde_results = self.cde_uploader.batch_upload_cde(
                        cde_df,
                        max_workers=10,
                        batch_size=25
                    )
                    results['cde'] = {
                        'records_uploaded': len(cde_df),
                        'upload_results': cde_results
                    }
                    print("✓ CDE data uploaded")
                else:
                    print("ℹ No CDE data to upload")
            
            print(f"\n{template.template_name.title()} workflow completed successfully!")
            return results
            
        except Exception as e:
            results['error'] = str(e)
            print(f"Error in {template.template_name if 'template' in locals() else 'unknown'} workflow: {str(e)}")
            raise


